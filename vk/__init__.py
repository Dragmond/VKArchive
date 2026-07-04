from __future__ import annotations

from dataclasses import dataclass

from database.database import db


@dataclass(slots=True)
class SessionUser:
    id: int
    first_name: str
    last_name: str
    photo: str | None = None


class SessionManager:
    """
    Управляет текущей VK-сессией приложения.
    Хранит токен и информацию о текущем пользователе.
    """

    TOKEN_KEY = "vk_access_token"

    def __init__(self):

        self._token = db.get_setting(self.TOKEN_KEY)

        self._user: SessionUser | None = None

    @property
    def token(self) -> str | None:

        return self._token

    @property
    def authorized(self) -> bool:

        return bool(self._token)

    @property
    def user(self) -> SessionUser | None:

        return self._user

    def login(self, token: str) -> None:

        token = token.strip()

        if not token:
            raise ValueError("Token is empty.")

        self._token = token

        db.set_setting(self.TOKEN_KEY, token)

    def set_user(
        self,
        *,
        id: int,
        first_name: str,
        last_name: str,
        photo: str | None = None,
    ) -> None:

        self._user = SessionUser(
            id=id,
            first_name=first_name,
            last_name=last_name,
            photo=photo,
        )

    def clear_user(self) -> None:

        self._user = None

    def logout(self) -> None:

        self._token = None

        self._user = None

        db.delete_setting(self.TOKEN_KEY)


session = SessionManager()
