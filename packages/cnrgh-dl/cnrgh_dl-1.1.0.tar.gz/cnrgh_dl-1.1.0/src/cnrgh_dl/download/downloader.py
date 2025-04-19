import shutil
from pathlib import Path
from time import sleep

import requests
import urllib3.exceptions
from tqdm import tqdm
from typing_extensions import Self

from cnrgh_dl import config
from cnrgh_dl.auth.refresh_token import (
    RefreshTokenThread,
    RefreshTokenThreadExitStatus,
)
from cnrgh_dl.download.url import Url
from cnrgh_dl.exceptions import PrematureDownloadTerminationError
from cnrgh_dl.logger import Logger
from cnrgh_dl.models import (
    FileType,
    LocalFile,
    RemoteFile,
    Result,
    Results,
    Status,
)
from cnrgh_dl.utils import hash_access_token, safe_parse_obj_as

logger = Logger.get_instance()
"""Module logger instance."""


class Downloader:
    """Handle the downloads."""

    _refresh_token_thread: RefreshTokenThread
    """A RefreshTokenThread instance to obtain a valid access token to
    include in each request made to the datawebnode server."""
    _output_dir: Path
    """Output directory where downloaded files are stored."""

    def __init__(
        self: Self,
        refresh_token_thread: RefreshTokenThread,
        output_dir: Path,
    ) -> None:
        """Initialize a downloader with a refresh token thread and
        an output directory to store files.
        """
        self._refresh_token_thread = refresh_token_thread
        self._output_dir = output_dir

    def _get_md5_from_project(self: Self, project_name: str) -> set[str]:
        """By using the project API endpoint with a project name,
        the server returns a JSON list of all the files contained within this project directory.
        We then only keep files with an ``.md5`` extension.

        :param project_name: The name of the project for which we want to retrieve the
            list of MD5 checksum file URLs.
        :return: A set of MD5 checksum file URLs present inside the directory.
        """
        retrieved_md5s: set[str] = set()
        files = []

        try:
            response = requests.get(
                config.DATAWEBNODE_PROJECT_FILES_ENDPOINT + project_name,
                headers={
                    "Authorization": f"Bearer {self._refresh_token_thread.token_response.access_token}",
                },
                timeout=config.REQUESTS_TIMEOUT,
            )
            response.raise_for_status()
            files = safe_parse_obj_as(list[RemoteFile], response.json())

        except requests.exceptions.RequestException as e:
            logger.error(
                "Could not retrieve the MD5 checksum file list for project %s from the server, "
                "which prevents downloading any additional checksum files: %s",
                project_name,
                e,
            )

        for file in files:
            if Url.get_path_extension(file.display_path) == ".md5":
                retrieved_md5s.add(file.display_path)

        return retrieved_md5s

    def fetch_additional_checksums(
        self: Self,
        urls: set[str],
    ) -> dict[str, LocalFile]:
        """For a given set of file URLs, retrieve their checksums from the datawebnode server if they exist.

        :param urls: A set of URLs for which we want to retrieve their checksums.
        :return: A queue of the found checksums. It is a dict containing as keys URLs of files to download and
            as values LocalFile instances containing metadata about the file that will be downloaded.
        """
        additional_checksum_urls: dict[str, LocalFile] = {}
        relative_file_paths: set[str] = set()
        project_names: set[str] = set()

        # 1. Obtain a set of project names.
        for url in urls:
            relative_file_path = url[
                len(config.DATAWEBNODE_DOWNLOAD_ENDPOINT) :
            ]
            relative_file_paths.add(relative_file_path)
            project_name = relative_file_path.split("/")[0]
            project_names.add(project_name)

        # 2. From the API, retrieve for each project
        # the list of files it contains and add only the MD5 files to a set.
        md5s_available: set[str] = set()
        for project_name in project_names:
            md5s_available.update(self._get_md5_from_project(project_name))

        # 3. If a file in the download list matches a MD5,
        # we add the MD5 to the download list.
        for relative_file_path in relative_file_paths:
            checksum_path = f"{relative_file_path}.md5"
            if checksum_path in md5s_available:
                filename = checksum_path.rsplit("/")[-1]
                filepath = Path(self._output_dir / filename)
                is_partially_downloaded = False

                additional_checksum_urls[
                    config.DATAWEBNODE_DOWNLOAD_ENDPOINT + checksum_path
                ] = LocalFile(
                    filename,
                    FileType.CHECKSUM,
                    filepath,
                    is_partially_downloaded,
                )

        return additional_checksum_urls

    def _download(
        self: Self,
        url: str,
        local_file: LocalFile,
        *,
        force_download: bool,
    ) -> None:
        """Download a file from the datawebnode server.
        This function can also continue a partial download by sending a Range header to the server
        if ``local_file.is_partially_downloaded`` is ``True``.

        :param url: The URL of the file to download,
            hosted on the datawebnode server.
        :param local_file: A LocalFile instance containing metadata about the file that will be downloaded.
        :param force_download: Flag to force the download of files.
        :raises requests.exceptions.RequestException:
            An error occurred while requesting the file.
        :raises requests.RequestException:
            An error occurred while handling the download request.
        :raises urllib3.exceptions.ReadTimeoutError:
            The network connection was lost while receiving a file.
        :raises PrematureDownloadTerminationError:
            The download could not fully finish because the server went down.
        :raises FileNotFoundError:
            The file was moved or deleted during the download.
        :raises Exception:
            An exception other than those listed above has been raised.
        """
        logger.debug(
            "Download is using access token '%s'.",
            hash_access_token(
                self._refresh_token_thread.token_response.access_token
            ),
        )
        partial_save_path = local_file.path.with_suffix(
            local_file.path.suffix + config.PARTIAL_DOWNLOAD_SUFFIX,
        )

        headers = {
            "Authorization": f"Bearer {self._refresh_token_thread.token_response.access_token}",
        }
        open_mode = "wb"

        if local_file.is_partially_downloaded:
            if force_download:
                partial_save_path.unlink(missing_ok=True)
            else:
                downloaded_size = partial_save_path.stat().st_size
                headers["Range"] = f"bytes={downloaded_size}-"
                open_mode = "ab"

        response = requests.get(
            url,
            stream=True,
            headers=headers,
            timeout=config.REQUESTS_TIMEOUT,
        )
        response.raise_for_status()

        file_size = int(response.headers.get("Content-Length", 0))

        desc = (
            f"{local_file.filename} (unknown total file size)"
            if file_size == 0
            else f"{local_file.filename}"
        )

        with (
            tqdm.wrapattr(
                response.raw,
                "read",
                total=file_size,
                unit="B",
                unit_scale=True,
                miniters=1,
                desc=desc,
                leave=False,
            ) as r_raw,
            Path.open(partial_save_path, open_mode) as f,
        ):
            shutil.copyfileobj(r_raw, f, length=16 * 1024 * 1024)

        # If the server goes down during a download,
        # raise an exception because the file has not been fully downloaded.
        if partial_save_path.stat().st_size < file_size:
            raise PrematureDownloadTerminationError

        partial_save_path.rename(local_file.path)

    def _pre_download_checks(
        self, url: str, local_file: LocalFile, *, force_download: bool
    ) -> Results:
        """Succession of checks to run before starting a download:
            - do not start the download if the file already exist in the output directory,
                and we are not forcing downloads.
            - do not start the download if the token refresh thread has encountered an error
                (offline session max duration was reached, or the token could not be refreshed).

        :param url: URL of the file to download.
        :param local_file: Metadata about the file that will be downloaded.
        :param force_download: Flag to force the download of files.
        :return: An empty dict if all the checks were successful,
          or a dict with the file URL as key and a Result
          instance as value containing details of the failed check error.
        """
        is_file_download_complete = (
            local_file.path.is_file() and not local_file.is_partially_downloaded
        )

        if not force_download and is_file_download_complete:
            logger.warning(
                "Skipping download of file %s as it already exists in the output directory.",
                str(local_file.filename),
            )
            return {
                url: Result(
                    local_file.filename,
                    local_file.file_type,
                    Status.SKIPPED,
                    "File already exists in the output directory.",
                ),
            }

        if (
            not self._refresh_token_thread.is_alive()
            and self._refresh_token_thread.exit_status
            == RefreshTokenThreadExitStatus.OFFLINE_SESSION_MAX_REACHED_ERROR
        ):
            logger.warning(
                "Skipping download of file %s as "
                "the maximum duration for an offline session was reached.",
                str(local_file.filename),
            )
            return {
                url: Result(
                    local_file.filename,
                    local_file.file_type,
                    Status.SKIPPED,
                    "Maximum duration for an offline session reached.",
                ),
            }

        if (
            not self._refresh_token_thread.is_alive()
            and self._refresh_token_thread.exit_status
            == RefreshTokenThreadExitStatus.REFRESH_TOKEN_ERROR
        ):
            logger.error(
                "File %s could not be downloaded as there was an error trying to obtain a new access token.",
                str(local_file.filename),
            )
            return {
                url: Result(
                    local_file.filename,
                    local_file.file_type,
                    Status.ERROR,
                    "Could not obtain a new access token to download the file.",
                ),
            }

        return {}

    def download_queue(
        self: Self,
        queue: dict[str, LocalFile],
        *,
        force_download: bool,
    ) -> Results:
        """Download a queue of URLs.

        :param queue: A dict containing as keys URLs of files to download and
            as values LocalFile instances containing metadata about the file that will be downloaded.
        :param force_download: Flag to force the download of files.
        :return: A dict containing as keys files URLs and as values error messages.
        """
        dl_results = {}

        for url in sorted(queue.keys()):
            local_file = queue[url]

            check_result = self._pre_download_checks(
                url, local_file, force_download=force_download
            )
            if check_result:
                dl_results.update(check_result)
                continue

            try:
                logger.info("Starting download of %s.", queue[url].filename)
                self._download(url, queue[url], force_download=force_download)
                logger.info("%s successfully downloaded.", queue[url].filename)
                dl_results.update(
                    {
                        url: Result(
                            local_file.filename,
                            local_file.file_type,
                            Status.SUCCESS,
                            "File successfully downloaded.",
                        ),
                    },
                )
                # Sleep to simulate a large download.
                if config.DOWNLOAD_WAIT_AFTER_COMPLETE > 0:
                    logger.debug(
                        "Download completed, will sleep %s seconds before moving to the next one.",
                        config.DOWNLOAD_WAIT_AFTER_COMPLETE,
                    )
                    sleep(config.DOWNLOAD_WAIT_AFTER_COMPLETE)

            except requests.RequestException as err:
                dl_results.update(
                    {
                        url: Result(
                            local_file.filename,
                            local_file.file_type,
                            Status.ERROR,
                            "An error occurred while handling the download request.",
                        ),
                    },
                )
                logger.error(err)
            except urllib3.exceptions.ReadTimeoutError as err:
                dl_results.update(
                    {
                        url: Result(
                            local_file.filename,
                            local_file.file_type,
                            Status.ERROR,
                            "Read timed out.",
                        ),
                    },
                )
                logger.error(err)
            except PrematureDownloadTerminationError as err:
                dl_results.update(
                    {
                        url: Result(
                            local_file.filename,
                            local_file.file_type,
                            Status.ERROR,
                            "Download could not fully finish.",
                        ),
                    },
                )
                logger.error(err)
            except FileNotFoundError as err:
                dl_results.update(
                    {
                        url: Result(
                            local_file.filename,
                            local_file.file_type,
                            Status.ERROR,
                            "File was moved or deleted during the download.",
                        ),
                    },
                )
                logger.error(err)
            except Exception as err:  # noqa: BLE001
                dl_results.update(
                    {
                        url: Result(
                            local_file.filename,
                            local_file.file_type,
                            Status.ERROR,
                            "An error occurred.",
                        ),
                    },
                )
                logger.error(err)

        return dl_results
