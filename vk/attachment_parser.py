from __future__ import annotations


class AttachmentParser:

    def parse(
        self,
        attachments: list[dict],
    ) -> list[dict]:

        result: list[dict] = []

        for attachment in attachments:

            if not isinstance(
                attachment,
                dict,
            ):
                continue

            attachment_type = attachment.get(
                "type",
                "",
            )

            data = attachment.get(
                attachment_type,
                {},
            )

            item = {
                "type": attachment_type,
                "data": data,
                "id": data.get("id"),
                "owner_id": data.get("owner_id"),
                "title": data.get("title"),
                "url": data.get("url"),
            }

            if attachment_type == "photo":

                sizes = data.get(
                    "sizes",
                    [],
                )

                if sizes:

                    largest = max(
                        sizes,
                        key=lambda size: (
                            size.get("width", 0),
                            size.get("height", 0),
                        ),
                    )

                    item["url"] = largest.get(
                        "url",
                        item["url"],
                    )

                    item["width"] = largest.get("width")

                    item["height"] = largest.get("height")

            elif attachment_type == "doc":

                item["ext"] = data.get("ext")

                item["size"] = data.get("size")

            elif attachment_type == "audio":

                item["artist"] = data.get("artist")

                item["duration"] = data.get("duration")

            elif attachment_type == "video":

                item["duration"] = data.get("duration")

                images = data.get(
                    "image",
                    [],
                )

                if images:

                    preview = max(
                        images,
                        key=lambda image: image.get(
                            "width",
                            0,
                        ),
                    )

                    item["preview"] = preview.get("url")

            result.append(item)

        return result


attachment_parser = AttachmentParser()
