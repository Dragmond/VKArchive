from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

import httpx

from media import MediaFile
from utils.config import config


class DownloadManager:

    def __init__(self) -> None:

        self._client = httpx.Client(
            timeout=60,
            follow_redirects=True,
        )

    def download(
        self,
        media: MediaFile,
        destination: Path,
    ) -> Path:

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
            return output

        with self._client.stream(
            "GET",
            media.url,
        ) as response:

            response.raise_for_status()

            with output.open("wb") as file:

                for chunk in response.iter_bytes(64 * 1024):

                    if chunk:

                        file.write(chunk)

        return output

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

        with ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="download",
        ) as executor:

            futures = [
                executor.submit(
                    self.download,
                    media,
                    destination,
                )
                for media in files
            ]

            for future in as_completed(futures):

                result.append(
                    future.result()
                )

        return result

    def close(self) -> None:

        self._client.close()


download_manager = DownloadManager()
