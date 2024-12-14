# modules discords
import discord
from discord.ext import commands, tasks

# modules cogs
from datas import datas

# models
from model.EpicGamesGames import EpicGamesGames
from model.EpicGamesServer import EpicGamesServer

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


def startup():
    EpicGamesServer.init()
    EpicGamesGames.init()


@bot.event
async def on_ready():
    try:
        await bot.load_extension("cogs.epicgames.epicgames")
        synced = await bot.tree.sync()
        print(f"synced {len(synced) } command(s)")
    except Exception as e:
        print(e)
    general_check.start()


async def epic_check() -> None:
    previous_free_games = set(EpicGamesGames.get_last_games())
    new_free_games = [
        *filter(
            lambda x: not x.title in previous_free_games,
            EpicGamesGames.scrap_free_games(),
        )
    ]
    new_free_games_title = [*map(lambda x: x.title, new_free_games)]
    if not new_free_games:
        return

    for serv in EpicGamesServer.get_valid_servers():
        assert serv.channel_id != None
        epic_channel = bot.get_channel(serv.channel_id)
        if not isinstance(epic_channel, discord.TextChannel):
            print(f"server channel {serv.channel_id} is not a textchannel")
            continue

        must_mention = serv.must_mention(new_free_games_title)
        if must_mention:
            assert serv.role_id != None
            await epic_channel.send(f"<@&{serv.role_id}>")
        for new_game in new_free_games:
            await epic_channel.send(new_game.title + "\n" + new_game.description)
            await epic_channel.send(new_game.img_link)

    EpicGamesGames.unlast_all()
    for game in new_free_games_title:
        EpicGamesGames.add_game(game)
    for game in new_free_games_title:
        EpicGamesGames.set_game_as_last(game)


@tasks.loop(hours=1)
async def general_check() -> None:
    await epic_check()


startup()
bot.run(datas.BOT_TOKEN)
