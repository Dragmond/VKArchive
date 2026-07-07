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

            result.append(
                {
                    "type": attachment_type,
                    "data": data,
                    "id": data.get("id"),
                    "owner_id": data.get("owner_id"),
                    "title": data.get("title"),
                    "url": data.get("url"),
                }
            )

        return result


attachment_parser = AttachmentParser()
