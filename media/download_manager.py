from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import httpx

from media import MediaFile


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

            filename = Path(path).name

            if not filename:
                filename = "file.bin"

        output = destination / filename

        with self._client.stream(
            "GET",
            media.url,
        ) as response:

            response.raise_for_status()

            with output.open("wb") as file:

                for chunk in response.iter_bytes(1024 * 64):

                    if chunk:

                        file.write(chunk)

        return output

    def download_many(
        self,
        files: list[MediaFile],
        destination: Path,
    ) -> list[Path]:

        result: list[Path] = []

        for media in files:

            result.append(
                self.download(
                    media,
                    destination,
                )
            )

        return result

    def close(self) -> None:

        self._client.close()


download_manager = DownloadManager()
