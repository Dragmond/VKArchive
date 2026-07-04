from database.database import db


class SessionManager:
    """
    Управляет текущей VK-сессией приложения.

    На данном этапе отвечает только за хранение и получение токена.
    Проверка токена через VK API будет добавлена следующим коммитом.
    """

    TOKEN_KEY = "vk_access_token"

    def __init__(self):

        self._token = db.get_setting(self.TOKEN_KEY)

    @property
    def token(self) -> str | None:

        return self._token

    @property
    def authorized(self) -> bool:

        return bool(self._token)

    def login(self, token: str) -> None:

        token = token.strip()

        if not token:
            raise ValueError("Token is empty.")

        self._token = token

        db.set_setting(self.TOKEN_KEY, token)

    def logout(self) -> None:

        self._token = None

        db.delete_setting(self.TOKEN_KEY)


session = SessionManager()
