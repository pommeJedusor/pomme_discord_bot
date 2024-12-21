from typing import List, Optional, Self

from model.Connection import DbConnection


class EpicGamesServer:
    def __init__(
        self, id: int, role_id: Optional[int], channel_id: Optional[int]
    ) -> None:
        self.id = id
        self.role_id = role_id
        self.channel_id = channel_id

    @classmethod
    def get_valid_servers(cls) -> List[Self]:
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT `id`, `role_id`, `channel_id`  FROM `epic_games_server` WHERE `channel_id` IS NOT NULL"
        )
        games = cursor.fetchall()

        cursor.close()
        return [cls(game[0], game[1], game[2]) for game in games]

    @classmethod
    def insert_server(cls, server_id: int) -> None:
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO `epic_games_server` (`id`) VALUES(?)", (server_id,)
        )
        connection.commit()

        cursor.close()

    @staticmethod
    def get_servers_to_mention(servers: List[int], games: List[str]) -> set[int]:
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        game_parameters_sql = "(" + (",".join(["?" for _ in games])) + ")"
        server_parameters_sql = "(" + (",".join(["?" for _ in servers])) + ")"
        query = f"SELECT `server_id`, COUNT(*) FROM `epic_games_server_has_seen_game` WHERE `server_id` IN {server_parameters_sql} AND `game_name` IN {game_parameters_sql} GROUP BY `server_id`"
        cursor.execute(query, (*servers, *games))
        results = cursor.fetchall()
        cursor.close()

        servers_set = set(servers)
        for result in filter(lambda x: x[1] == len(games), results):
            servers_set.remove(result[0])
        return servers_set

    @staticmethod
    def set_channel_id(server_id: int, channel_id: int):
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE `epic_games_server` SET `channel_id` = ? WHERE `id` = ?",
            (channel_id, server_id),
        )
        connection.commit()

        cursor.close()

    @staticmethod
    def set_role_id(server_id: int, role_id: int):
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE `epic_games_server` SET `role_id` = ? WHERE `id` = ?",
            (role_id, server_id),
        )
        connection.commit()

        cursor.close()

    @staticmethod
    def init():
        connection = DbConnection.get_connection()
        cursor = connection.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS epic_games_server_has_seen_game (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_name TEXT NOT NULL,
                server_id BIGINT NOT NULL,
                UNIQUE(game_name, server_id)
            );
        """
        cursor.execute(sql)
        connection.commit()

        sql = """
            CREATE TABLE IF NOT EXISTS epic_games_server (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_id BIGINT NULL,
                channel_id BIGINT NULL,
                UNIQUE(role_id, channel_id)
            );
        """
        cursor.execute(sql)
        connection.commit()

        cursor.close()
