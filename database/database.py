from pathlib import Path
import sqlite3


DATABASE = Path("vkarchive.db")


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE)

        self.cursor = self.connection.cursor()

        self.create()

    def create(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings(

            key TEXT PRIMARY KEY,

            value TEXT
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

        self.connection.commit()


db = Database()
