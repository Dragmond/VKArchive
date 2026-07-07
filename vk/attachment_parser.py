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

            result.append(
                {
                    "type": attachment.get("type"),
                    "data": attachment.get(
                        attachment.get(
                            "type",
                            "",
                        ),
                        {},
                    ),
                }
            )

        return result


attachment_parser = AttachmentParser()
