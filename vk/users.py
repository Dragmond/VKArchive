from __future__ import annotations

from vk.client import client
from vk.user import User


class UsersService:

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

        response = client.request(
            "users.get",
            user_ids=",".join(
                map(str, ids),
            ),
            fields="photo_100",
        )

        result: dict[int, User] = {}

        for item in response:

            user = User(
                id=item["id"],
                first_name=item["first_name"],
                last_name=item["last_name"],
                photo=item.get("photo_100"),
            )

            result[user.id] = user

        return result


users = UsersService()
