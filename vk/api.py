from __future__ import annotations

from typing import Any

import requests


class VKApiError(Exception):
    pass


class VKApi:

    API_VERSION = "5.199"

    def __init__(self, access_token: str) -> None:

        self._token = access_token

    def call(
        self,
        method: str,
        **params,
    ) -> dict[str, Any]:

        response = requests.get(
            f"https://api.vk.com/method/{method}",
            params={
                **params,
                "access_token": self._token,
                "v": self.API_VERSION,
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:

            raise VKApiError(
                data["error"].get(
                    "error_msg",
                    "Unknown VK API error",
                )
            )

        return data["response"]

    def get_profile(self) -> dict[str, Any]:

        profile = self.call(
            "users.get",
        )

        return profile[0]

    def get_dialogs(
        self,
        count: int = 200,
        offset: int = 0,
    ) -> dict[str, Any]:

        return self.call(
            "messages.getConversations",
            count=count,
            offset=offset,
        )

    def get_history(
        self,
        peer_id: int,
        count: int = 200,
        offset: int = 0,
    ) -> dict[str, Any]:

        return self.call(
            "messages.getHistory",
            peer_id=peer_id,
            count=count,
            offset=offset,
        )
