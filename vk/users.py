from __future__ import annotations

from vk.client import client
from vk.user import User


class UsersService:

    def __init__(self) -> None:

        self._cache: dict[int, User] = {}

    def get(
        self,
        user_ids: list[int],
    ) -> dict[int, User]:

        ids = sorted(
            {
                user_id
                for user_id in user_ids
                if user_id > 0
            }
        )

        if not ids:
            return {}

        result: dict[int, User] = {}

        missing: list[int] = []

        for user_id in ids:

            cached = self._cache.get(
                user_id,
            )

            if cached is None:

                missing.append(
                    user_id,
                )

            else:

                result[user_id] = cached

        if missing:

            response = client.request(
                "users.get",
                user_ids=",".join(
                    map(
                        str,
                        missing,
                    )
                ),
                fields="photo_100",
            )

            for item in response:

                user = User(
                    id=item["id"],
                    first_name=item["first_name"],
                    last_name=item["last_name"],
                    photo=item.get(
                        "photo_100",
                    ),
                )

                self._cache[user.id] = user

                result[user.id] = user

        return result

    def clear_cache(
        self,
    ) -> None:

        self._cache.clear()


users = UsersService()
