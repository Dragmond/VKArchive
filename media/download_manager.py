from __future__ import annotations

import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse

import httpx

from media import MediaFile
from utils.config import config


ProgressCallback = Callable[[int, int, MediaFile], None]


class DownloadManager:

    MAX_RETRIES = 3

    def __init__(self) -> None:

        self._client = httpx.Client(
            timeout=60,
            follow_redirects=True,
        )

        self._downloaded_urls: dict[str, Path] = {}

        self._hash_cache: dict[str, Path] = {}

        self._progress_callback: ProgressCallback | None = None

    def set_progress_callback(
        self,
        callback: ProgressCallback | None,
    ) -> None:

        self._progress_callback = callback

    def _notify_progress(
        self,
        current: int,
        total: int,
        media: MediaFile,
    ) -> None:

        if self._progress_callback is None:
            return

        self._progress_callback(
            current,
            total,
            media,
        )

    def _sha256(
        self,
        path: Path,
    ) -> str:

        sha = hashlib.sha256()

        with path.open("rb") as file:

            while True:

                chunk = file.read(1024 * 1024)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()

    def _download_once(
        self,
        media: MediaFile,
        destination: Path,
    ) -> Path:

        cached = self._downloaded_urls.get(media.url)

        if cached is not None and cached.exists():
            return cached

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = media.filename

        if not filename:

            path = urlparse(media.url).path

            filename = Path(path).name or "file.bin"

        output = destination / filename

        if (
            config.settings.continue_download
            and output.exists()
        ):
            digest = self._sha256(output)

            self._downloaded_urls[media.url] = output

            self._hash_cache[digest] = output

            return output

        headers = {}

        mode = "wb"

        downloaded = 0

        if output.exists():

            downloaded = output.stat().st_size

            if downloaded > 0:

                headers["Range"] = f"bytes={downloaded}-"

                mode = "ab"

        with self._client.stream(
            "GET",
            media.url,
            headers=headers,
        ) as response:

            if headers and response.status_code != 206:
                downloaded = 0
                mode = "wb"

            response.raise_for_status()

            expected_size = None

            if response.headers.get("Content-Length"):

                expected_size = int(
                    response.headers["Content-Length"]
                )

                if response.status_code == 206:
                    expected_size += downloaded

            with output.open(mode) as file:

                for chunk in response.iter_bytes(
                    64 * 1024
                ):

                    if chunk:
                        file.write(chunk)

        if (
            expected_size is not None
            and output.stat().st_size != expected_size
        ):

            output.unlink(missing_ok=True)

            raise IOError(
                f"Incomplete download: {filename}"
            )

        digest = self._sha256(output)

        duplicate = self._hash_cache.get(digest)

        if (
            duplicate is not None
            and duplicate.exists()
            and duplicate != output
        ):

            output.unlink(missing_ok=True)

            self._downloaded_urls[media.url] = duplicate

            return duplicate

        self._hash_cache[digest] = output

        self._downloaded_urls[media.url] = output

        return output

    def download(
        self,
        media: MediaFile,
        destination: Path,
    ) -> Path:

        last_error: Exception | None = None

        for attempt in range(self.MAX_RETRIES):

            try:

                return self._download_once(
                    media,
                    destination,
                )

            except (
                httpx.HTTPError,
                IOError,
            ) as error:

                last_error = error

                if attempt + 1 == self.MAX_RETRIES:
                    break

                time.sleep(2**attempt)

        raise last_error

    def download_many(
        self,
        files: list[MediaFile],
        destination: Path,
    ) -> list[Path]:

        result: list[Path] = []

        workers = max(
            1,
            config.settings.threads,
        )

        total = len(files)

        completed = 0

        with ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="download",
        ) as executor:

            future_map = {
                executor.submit(
                    self.download,
                    media,
                    destination,
                ): media
                for media in files
            }

            for future in as_completed(future_map):

                media = future_map[future]

                result.append(
                    future.result()
                )

                completed += 1

                self._notify_progress(
                    completed,
                    total,
                    media,
                )

        return result

    def clear_cache(self) -> None:

        self._downloaded_urls.clear()

        self._hash_cache.clear()

    def close(self) -> None:

        self.clear_cache()

        self._client.close()


download_manager = DownloadManager()
