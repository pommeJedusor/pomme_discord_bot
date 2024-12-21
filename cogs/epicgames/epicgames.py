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
            title = "Erreur"
            description = "echec lors de la récupération de l'id du server"
            color = 0xFF0000
        elif channel_id == None:
            title = "Erreur"
            description = "echec lors de la récupération de l'id du channel"
            color = 0xFF0000
        else:
            title = "Réussite"
            description = "l'id du channel a été mis à jour"
            color = 0x00FF00
            EpicGamesServer.insert_server(guild_id)
            EpicGamesServer.set_channel_id(guild_id, channel_id)

        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

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
            title = "Erreur"
            description = "echec lors de la récupération de l'id du server"
            color = 0xFF0000
        else:
            EpicGamesServer.insert_server(guild_id)
            EpicGamesServer.set_role_id(guild_id, role_id)
            title = "Réussite"
            description = "l'id du role a été mis à jour"
            color = 0x00FF00

        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @epicgames_set_channel.error
    @epicgames_set_role.error
    async def epicgames_error(self, interaction: discord.Interaction, error):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(
                "vous n'avez pas les permissions requises", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "une erreur est survenue", ephemeral=True
            )
            print("|ERROR| ", error)


async def setup(bot):
    await bot.add_cog(EpicGames(bot))
