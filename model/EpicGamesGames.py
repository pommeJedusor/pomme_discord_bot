import requests, json
from typing import List, Self

from model.Connection import DbConnection
from model.HttpRequest import HttpRequest

def get_element_slug(element):
    try:
        slug = element["catalogNs"]["mappings"][0]["pageSlug"]
        if slug:
            return slug
    except:
        pass
    try:
        slug = element["offerMappings"][0]["pageSlug"]
        if slug:
            return slug
    except:
        pass
    return element["productSlug"]


class EpicGamesGames:
    def __init__(self, title: str, description: str, img_link: str, slug: str) -> None:
        self.title = title
        self.description = description
        self.img_link = img_link
        self.slug = slug

    @staticmethod
    def get_last_games() -> list[str]:
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT `name` FROM `epic_games_games` WHERE `is_last` = 1")
        games = cursor.fetchall()

        cursor.close()
        return [game[0] for game in games]

    @staticmethod
    def unlast_all() -> None:
        """
        deactivate is_last for all games
        """
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE `epic_games_games` SET `is_last` = 0 WHERE `is_last` = 1"
        )
        connection.commit()

        cursor.close()

    @staticmethod
    def add_games(names: List[str], is_last: bool = True) -> None:
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        games = [(None, name, is_last) for name in names]
        paramaters = [x for game in games for x in game]

        sql_parameters = ",".join(["(?,?,?)" for _ in names])
        cursor.execute(
            f"INSERT OR IGNORE INTO `epic_games_games` (`id`, `name`, `is_last`) VALUES{sql_parameters}",
            (*paramaters,),
        )
        connection.commit()

        cursor.close()

    @staticmethod
    def set_games_as_last(names: List[str]) -> None:
        connection = DbConnection.get_connection()
        cursor = connection.cursor()

        sql_parameters = "(" + ",".join(["?" for _ in names]) + ")"
        query = f"UPDATE `epic_games_games` SET `is_last` = 1 WHERE `name` IN {sql_parameters}"
        cursor.execute(query, (*names,))
        connection.commit()

        cursor.close()

    @classmethod
    def scrap_free_games(cls) -> List[Self]:
        r = requests.get(
            "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=fr-US&country=BE&allowCountries=BE"
        )
        if not r.ok:
            raise Exception(
                f"error during reception of the datas from epiceGames : {r.headers}"
            )
        HttpRequest.insert_http_request(r.text)

        free_games = []
        elements = json.loads(r.content)["data"]["Catalog"]["searchStore"]["elements"]
        is_free_game = (
            lambda x: x["promotions"]
            and x["promotions"]["promotionalOffers"]
            and 0 == x["price"]["totalPrice"]["discountPrice"]
        )
        free_games = filter(is_free_game, elements)
        free_games = map(
            lambda x: cls(
                x["title"],
                x["description"],
                x["keyImages"][0]["url"],
                get_element_slug(x),
            ),
            free_games,
        )

        return [*free_games]

    @staticmethod
    def init():
        connection = DbConnection.get_connection()
        cursor = connection.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS epic_games_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                is_last INTEGER NOT NULL
            );
        """
        cursor.execute(sql)
        connection.commit()

        cursor.close()
