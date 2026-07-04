from __future__ import annotations

from dataclasses import dataclass

import httpx

from vk import session


API_VERSION = "5.199"
API_URL = "https://api.vk.com/method/"


class VKError(Exception):
    """Базовое исключение VK API."""


class VKAuthorizationError(VKError):
    """Недействительный или отсутствующий токен."""


@dataclass(slots=True)
class VKUser:

    id: int

    first_name: str

    last_name: str

    photo: str | None = None


class VKClient:

    def __init__(self) -> None:

        self._client = httpx.Client(
            base_url=API_URL,
            timeout=30.0,
            follow_redirects=True,
        )

    def _request(self, method: str, **params):

        if not session.authorized:
            raise VKAuthorizationError("VK token is missing.")

        params["access_token"] = session.token
        params["v"] = API_VERSION

        response = self._client.get(
            method,
            params=params,
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:

            error = data["error"]

            raise VKAuthorizationError(
                f'VK API error {error["error_code"]}: {error["error_msg"]}'
            )

        return data["response"]

    def validate(self) -> VKUser:

        response = self._request(
            "users.get",
            fields="photo_200",
        )[0]

        return VKUser(
            id=response["id"],
            first_name=response["first_name"],
            last_name=response["last_name"],
            photo=response.get("photo_200"),
        )

    def close(self) -> None:

        self._client.close()


client = VKClient()
