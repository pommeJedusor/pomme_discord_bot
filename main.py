# modules discords
import os
from typing import cast
import discord
from discord.ext import commands, tasks

# models
from model.EpicGamesGames import EpicGamesGames
from model.EpicGamesServer import EpicGamesServer

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = cast(str, os.getenv("TOKEN"))
if BOT_TOKEN is None:
    print("Please set the token")
    exit()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def startup():
    EpicGamesServer.init()
    EpicGamesGames.init()


@bot.event
async def on_ready():
    try:
        await bot.load_extension("cogs.epicgames.epicgames")
        await bot.load_extension("cogs.help.help")
        synced = await bot.tree.sync()
        print(f"synced {len(synced) } command(s)")
    except Exception as e:
        print(e)
    general_check.start()


async def epic_check() -> None:
    previous_free_games = set(EpicGamesGames.get_last_games())
    try:
        new_free_games = [
            *filter(
                lambda x: not x.title in previous_free_games,
                EpicGamesGames.scrap_free_games(),
            )
        ]
    except Exception as e:
        print(f"failed to scrap games: {e}")
        return

    new_free_games_title = [*map(lambda x: x.title, new_free_games)]
    if not new_free_games:
        return

    servers_to_mention = EpicGamesServer.get_servers_to_mention(
        [server.id for server in EpicGamesServer.get_valid_servers()],
        new_free_games_title,
    )
    for serv in EpicGamesServer.get_valid_servers():
        assert serv.channel_id != None
        epic_channel = bot.get_channel(serv.channel_id)
        if not isinstance(epic_channel, discord.TextChannel):
            continue

        if serv.id in servers_to_mention and serv.role_id:
            assert serv.role_id != None
            await epic_channel.send(f"<@&{serv.role_id}>")
        for new_game in new_free_games:
            # sometimes the description of the game is also the title
            if new_game.title == new_game.description:
                await epic_channel.send(new_game.title)
            else:
                await epic_channel.send(new_game.title + "\n" + new_game.description)
            await epic_channel.send(new_game.img_link)

    EpicGamesGames.unlast_all()
    EpicGamesGames.add_games(new_free_games_title)
    EpicGamesGames.set_games_as_last(new_free_games_title)


@tasks.loop(hours=1)
async def general_check() -> None:
    await epic_check()


startup()
bot.run(BOT_TOKEN)
