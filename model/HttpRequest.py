from typing import List, Self

from model.Connection import DbConnection

class HttpRequest:
    def __init__(self, id: int, content: str) -> None:
        self.id = id
        self.content = content

    @classmethod
    def get_requests(cls) -> List[Self]:
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT `id`, `content` FROM `epicgames_http_request`")
        games = cursor.fetchall()

        cursor.close()
        return [cls(game[0], game[1]) for game in games]

    @classmethod
    def insert_http_request(cls, content: str) -> None:
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO `epicgames_http_request` (`id`, `content`) VALUES(?,?)", (None, content)
        )
        connection.commit()

        cursor.close()

    @staticmethod
    def init():
        connection = DbConnection.get_connection()
        cursor = connection.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS epicgames_http_request (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                UNIQUE(content)
            );
        """
        cursor.execute(sql)
        connection.commit()

        cursor.close()
