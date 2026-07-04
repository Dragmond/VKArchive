from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MediaFile:
    type: str
    url: str
    filename: str | None = None
    size: int | None = None


class AttachmentParser:
    """
    Преобразует вложения VK API в единый формат,
    который позже будет использоваться DownloadManager.
    """

    def parse(self, attachments: list[dict]) -> list[MediaFile]:

        result: list[MediaFile] = []

        for attachment in attachments:

            attachment_type = attachment["type"]

            parser = getattr(
                self,
                f"_parse_{attachment_type}",
                None,
            )

            if parser is None:
                continue

            result.extend(parser(attachment))

        return result

    def _parse_photo(
        self,
        attachment: dict,
    ) -> list[MediaFile]:

        photo = attachment["photo"]

        sizes = photo.get("sizes", [])

        if not sizes:
            return []

        best = max(
            sizes,
            key=lambda item: item["width"] * item["height"],
        )

        return [
            MediaFile(
                type="photo",
                url=best["url"],
            )
        ]

    def _parse_doc(
        self,
        attachment: dict,
    ) -> list[MediaFile]:

        document = attachment["doc"]

        return [
            MediaFile(
                type="doc",
                url=document["url"],
                filename=document.get("title"),
                size=document.get("size"),
            )
        ]

    def _parse_audio_message(
        self,
        attachment: dict,
    ) -> list[MediaFile]:

        voice = attachment["audio_message"]

        url = (
            voice.get("link_ogg")
            or voice.get("link_mp3")
        )

        if url is None:
            return []

        return [
            MediaFile(
                type="voice",
                url=url,
            )
        ]

    def _parse_video(
        self,
        attachment: dict,
    ) -> list[MediaFile]:

        video = attachment["video"]

        files = video.get("files", {})

        for quality in (
            "mp4_2160",
            "mp4_1440",
            "mp4_1080",
            "mp4_720",
            "mp4_480",
            "mp4_360",
            "external",
        ):
            if quality in files:
                return [
                    MediaFile(
                        type="video",
                        url=files[quality],
                    )
                ]

        return []


parser = AttachmentParser()
