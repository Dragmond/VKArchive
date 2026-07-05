from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(slots=True)
class VKSession:

    access_token: str
    user_id: int


class VKAuthService:

    def __init__(
        self,
        config_path: Path,
    ) -> None:

        self._config_path = config_path

    def has_session(self) -> bool:

        if not self._config_path.exists():
            return False

        try:

            data = json.loads(
                self._config_path.read_text(
                    encoding="utf-8",
                )
            )

        except Exception:

            return False

        return bool(
            data.get("access_token")
        )

    def load_session(self) -> VKSession | None:

        if not self.has_session():
            return None

        data = json.loads(
            self._config_path.read_text(
                encoding="utf-8",
            )
        )

        return VKSession(
            access_token=data["access_token"],
            user_id=int(
                data.get(
                    "user_id",
                    0,
                )
            ),
        )

    def save_session(
        self,
        session: VKSession,
    ) -> None:

        self._config_path.write_text(
            json.dumps(
                {
                    "access_token": session.access_token,
                    "user_id": session.user_id,
                },
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def clear_session(self) -> None:

        if self._config_path.exists():

            self._config_path.unlink()
