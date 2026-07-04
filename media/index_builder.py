from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from pathlib import Path


@dataclass(slots=True)
class ConversationIndex:

    name: str

    message_count: int

    last_message_date: int

    relative_path: str


class IndexBuilder:

    def __init__(self, root: Path):

        self._root = root

    def build(
        self,
        conversations: list[ConversationIndex],
    ) -> Path:

        output = self._root / "index.html"

        rows: list[str] = []

        conversations = sorted(
            conversations,
            key=lambda x: x.last_message_date,
            reverse=True,
        )

        for conversation in conversations:

            date = datetime.fromtimestamp(
                conversation.last_message_date
            ).strftime("%Y-%m-%d %H:%M")

            rows.append(
                f"""
<tr>
<td><a href="{escape(conversation.relative_path)}">{escape(conversation.name)}</a></td>
<td>{conversation.message_count}</td>
<td>{date}</td>
</tr>
""".strip()
            )

        html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VK Archive</title>

<style>

body{{
background:#202124;
color:#fff;
font-family:Segoe UI,Arial,sans-serif;
margin:40px;
}}

input{{
width:100%;
padding:10px;
margin-bottom:20px;
font-size:16px;
box-sizing:border-box;
}}

table{{
width:100%;
border-collapse:collapse;
}}

th,td{{
padding:10px;
border-bottom:1px solid #444;
}}

a{{
color:#8ab4f8;
text-decoration:none;
}}

</style>

</head>

<body>

<h1>VK Archive</h1>

<input
id="search"
placeholder="Поиск диалога..."
oninput="filter()">

<table id="dialogs">

<thead>

<tr>

<th>Диалог</th>

<th>Сообщений</th>

<th>Последнее сообщение</th>

</tr>

</thead>

<tbody>

{''.join(rows)}

</tbody>

</table>

<script>

function filter(){{
const value=document.getElementById("search").value.toLowerCase();

for(const row of document.querySelectorAll("#dialogs tbody tr")){{

const text=row.innerText.toLowerCase();

row.style.display=text.includes(value)?"":"none";

}}
}}

</script>

</body>

</html>
"""

        output.write_text(
            html,
            encoding="utf-8",
        )

        return output
