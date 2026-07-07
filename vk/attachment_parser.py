from __future__ import annotations

from vk.attachment import Attachment


class AttachmentParser:

    def parse(
        self,
        attachments: list[dict],
    ) -> list[Attachment]:

        result: list[Attachment] = []

        for attachment in attachments:

            if not isinstance(attachment, dict):
                continue

            attachment_type = attachment.get("type", "")
            data = attachment.get(attachment_type, {})

            item = Attachment(
                type=attachment_type,
                id=data.get("id"),
                owner_id=data.get("owner_id"),
                title=data.get("title"),
                url=data.get("url"),
                data=data,
            )

            if (
                item.owner_id is not None
                and item.id is not None
            ):
                item.vk_url = (
                    f"https://vk.com/"
                    f"{attachment_type}"
                    f"{item.owner_id}_{item.id}"
                )

            if attachment_type == "photo":

                sizes = data.get("sizes", [])

                if sizes:

                    largest = max(
                        sizes,
                        key=lambda s: (
                            s.get("width", 0),
                            s.get("height", 0),
                        ),
                    )

                    item.url = largest.get(
                        "url",
                        item.url,
                    )

                    item.extra["width"] = largest.get("width")
                    item.extra["height"] = largest.get("height")

            elif attachment_type == "video":

                images = data.get("image", [])

                if images:

                    preview = max(
                        images,
                        key=lambda x: x.get(
                            "width",
                            0,
                        ),
                    )

                    item.extra["preview"] = preview.get("url")

                item.extra["duration"] = data.get("duration")

            elif attachment_type == "audio":

                item.extra["artist"] = data.get("artist")
                item.extra["duration"] = data.get("duration")

            elif attachment_type == "doc":

                item.extra["ext"] = data.get("ext")
                item.extra["size"] = data.get("size")

            elif attachment_type == "link":

                item.url = data.get("url")

                item.title = (
                    data.get("title")
                    or data.get("caption")
                    or data.get("url")
                )

            elif attachment_type == "poll":

                item.title = data.get("question")

                item.extra["votes"] = data.get("votes")
                item.extra["answers"] = len(
                    data.get("answers", [])
                )

            elif attachment_type == "geo":

                item.title = data.get("coordinates")

                place = data.get("place")

                if place:

                    item.extra["place"] = place.get("title")

            elif attachment_type == "wall":

                item.extra["text"] = data.get("text")
                item.extra["from_id"] = data.get("from_id")

            elif attachment_type == "gift":

                item.title = (
                    data.get("description")
                    or "Подарок"
                )

                item.url = (
                    data.get("thumb_256")
                    or data.get("thumb_96")
                )

            elif attachment_type == "graffiti":

                item.url = data.get("url")

            elif attachment_type == "story":

                item.title = "История"

            elif attachment_type == "market":

                item.extra["price"] = (
                    data.get("price", {})
                    .get("text")
                )

            elif attachment_type == "call":

                item.extra["duration"] = data.get("duration")

            result.append(item)

        return result


attachment_parser = AttachmentParser()
