from __future__ import annotations


class AttachmentParser:

    def parse(
        self,
        attachments: list[dict],
    ) -> list[dict]:

        result: list[dict] = []

        for attachment in attachments:

            if not isinstance(attachment, dict):
                continue

            attachment_type = attachment.get("type", "")
            data = attachment.get(attachment_type, {})

            item = {
                "type": attachment_type,
                "data": data,
                "id": data.get("id"),
                "owner_id": data.get("owner_id"),
                "title": data.get("title"),
                "url": data.get("url"),
                "vk_url": None,
            }

            owner = data.get("owner_id")
            item_id = data.get("id")

            if (
                owner is not None
                and item_id is not None
            ):

                item["vk_url"] = (
                    f"https://vk.com/{attachment_type}"
                    f"{owner}_{item_id}"
                )

            if attachment_type == "photo":

                sizes = data.get("sizes", [])

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

            elif attachment_type == "video":

                images = data.get("image", [])

                if images:

                    preview = max(
                        images,
                        key=lambda image: image.get(
                            "width",
                            0,
                        ),
                    )

                    item["preview"] = preview.get("url")

                item["duration"] = data.get("duration")

            elif attachment_type == "audio":

                item["artist"] = data.get("artist")
                item["duration"] = data.get("duration")

            elif attachment_type == "doc":

                item["ext"] = data.get("ext")
                item["size"] = data.get("size")

            result.append(item)

        return result


attachment_parser = AttachmentParser()
