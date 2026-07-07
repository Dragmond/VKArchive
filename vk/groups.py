from __future__ import annotations

from vk.client import client
from vk.group import Group


class GroupsService:

    def __init__(self) -> None:

        self._cache: dict[int, Group] = {}

    def get(
        self,
        group_ids: list[int],
    ) -> dict[int, Group]:

        ids = sorted(
            {
                abs(group_id)
                for group_id in group_ids
                if group_id < 0
            }
        )

        if not ids:
            return {}

        result: dict[int, Group] = {}

        missing: list[int] = []

        for group_id in ids:

            cached = self._cache.get(group_id)

            if cached is None:
                missing.append(group_id)
            else:
                result[group_id] = cached

        if missing:

            response = client.request(
                "groups.getById",
                group_ids=",".join(
                    map(
                        str,
                        missing,
                    )
                ),
                fields="photo_100",
            )

            for item in response:

                group = Group(
                    id=item["id"],
                    name=item["name"],
                    photo=item.get("photo_100"),
                )

                self._cache[group.id] = group
                result[group.id] = group

        return result

    def clear_cache(
        self,
    ) -> None:

        self._cache.clear()


groups = GroupsService()
