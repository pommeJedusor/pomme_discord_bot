from discord import app_commands
import discord
from discord.app_commands.errors import MissingPermissions
from discord.ext import commands

from model.EpicGamesServer import EpicGamesServer


class EpicGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="epicgames_set_channel",
        description="les nouveaux jeux gratuits seront montré dans ce channel",
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def epicgames_set_channel(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id
        guild_id = interaction.guild_id
        if guild_id == None:
            await interaction.response.send_message(
                content=f"echec lors de la récupération de l'id du server"
            )
            return
        if channel_id == None:
            await interaction.response.send_message(
                content=f"echec lors de la récupération de l'id du channel"
            )
            return
        EpicGamesServer.insert_server(guild_id)
        EpicGamesServer.set_channel_id(guild_id, channel_id)
        await interaction.response.send_message(
            content=f"l'id du channel a été mis à jour"
        )

    @app_commands.command(
        name="epicgames_set_role",
        description="ce rôle seras mentionné lors de nouveaux jeux gratuits",
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def epicgames_set_role(
        self, interaction: discord.Interaction, role: discord.Role
    ):
        role_id = role.id
        guild_id = interaction.guild_id
        if guild_id == None:
            await interaction.response.send_message(
                content=f"echec lors de la récupération de l'id du server"
            )
            return
        EpicGamesServer.insert_server(guild_id)
        EpicGamesServer.set_role_id(guild_id, role_id)
        await interaction.response.send_message(
            content=f"l'id du role a été mis à jour"
        )

    @epicgames_set_channel.error
    @epicgames_set_role.error
    async def epicgames_set_channel_error(
        self, interaction: discord.Interaction, error
    ):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises"
            )
        else:
            await interaction.response.send_message("une erreur est survenue")
            print("|ERROR| ", error)


async def setup(bot):
    await bot.add_cog(EpicGames(bot))
