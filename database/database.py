from pathlib import Path
import sqlite3


DATABASE = Path("vkarchive.db")


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE)

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create()

    def create(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS downloads(
            id INTEGER PRIMARY KEY,
            url TEXT,
            sha256 TEXT,
            filename TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY,
            peer_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            date INTEGER NOT NULL,
            text TEXT NOT NULL,
            outgoing INTEGER NOT NULL
        )
        """)

        self.connection.commit()

    def set_setting(self, key: str, value: str) -> None:

        self.cursor.execute(
            """
            INSERT INTO settings(key, value)
            VALUES(?, ?)
            ON CONFLICT(key)
            DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )

        self.connection.commit()

    def get_setting(self, key: str, default=None):

        row = self.cursor.execute(
            """
            SELECT value
            FROM settings
            WHERE key = ?
            """,
            (key,),
        ).fetchone()

        if row is None:
            return default

        return row["value"]

    def delete_setting(self, key: str) -> None:

        self.cursor.execute(
            """
            DELETE FROM settings
            WHERE key = ?
            """,
            (key,),
        )

        self.connection.commit()

    def has_setting(self, key: str) -> bool:

        row = self.cursor.execute(
            """
            SELECT 1
            FROM settings
            WHERE key = ?
            LIMIT 1
            """,
            (key,),
        ).fetchone()

        return row is not None

    def get_all_settings(self) -> dict[str, str]:

        rows = self.cursor.execute(
            """
            SELECT key, value
            FROM settings
            """
        ).fetchall()

        return {
            row["key"]: row["value"]
            for row in rows
        }

    def save_message(
        self,
        *,
        message_id: int,
        peer_id: int,
        sender_id: int,
        date: int,
        text: str,
        outgoing: bool,
    ) -> None:

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO messages(
                id,
                peer_id,
                sender_id,
                date,
                text,
                outgoing
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                message_id,
                peer_id,
                sender_id,
                date,
                text,
                int(outgoing),
            ),
        )

        self.connection.commit()

    def get_last_message_id(
        self,
        peer_id: int,
    ) -> int | None:

        row = self.cursor.execute(
            """
            SELECT MAX(id) AS id
            FROM messages
            WHERE peer_id = ?
            """,
            (peer_id,),
        ).fetchone()

        if row is None:
            return None

        return row["id"]

    def close(self):

        self.connection.close()


db = Database()
