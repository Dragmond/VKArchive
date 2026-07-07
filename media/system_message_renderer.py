from __future__ import annotations


class SystemMessageRenderer:

    _ACTION_TEXT: dict[str, str] = {
        "chat_create": "Создана беседа",
        "chat_title_update": "Изменено название беседы",
        "chat_photo_update": "Обновлена фотография беседы",
        "chat_photo_remove": "Удалена фотография беседы",
        "chat_invite_user": "Приглашён участник",
        "chat_invite_user_by_link": "Участник присоединился по ссылке",
        "chat_kick_user": "Участник покинул беседу",
        "pin_message": "Закреплено сообщение",
        "unpin_message": "Сообщение откреплено",
    }

    def render(
        self,
        action: dict | None,
    ) -> str:

        if not action:
            return ""

        action_type = action.get("type", "")

        text = self._ACTION_TEXT.get(
            action_type,
            action_type or "Системное событие",
        )

        member = action.get("member_id")

        if member is not None:
            text += f" (ID {member})"

        new_title = action.get("text")

        if new_title:
            text += f": {new_title}"

        return (
            "<div class='system-message'>"
            f"ℹ️ {text}"
            "</div>"
        )
