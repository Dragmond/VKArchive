from __future__ import annotations

from media import MediaFile
from vk.attachment import Attachment


class MediaMapper:

    def map(
        self,
        attachments: list[Attachment],
    ) -> list[MediaFile]:

        result: list[MediaFile] = []

        for attachment in attachments:

            url = attachment.url

            if not url:
                continue

            result.append(
                MediaFile(
                    type=attachment.type,
                    url=url,
                    filename=attachment.title,
                    size=attachment.extra.get(
                        "size",
                    ),
                )
            )

        return result


media_mapper = MediaMapper()
