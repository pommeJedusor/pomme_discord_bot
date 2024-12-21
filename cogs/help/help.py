from typing import Optional
from discord import app_commands
import discord
from discord.ext import commands

from cogs.help.command_description import (
    CommandNotFoundException,
    get_command_description,
)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="liste des commandes ou leurs déscriptions",
    )
    async def help(self, interaction: discord.Interaction, command: Optional[str]):

        if command:
            try:
                title = command
                description = get_command_description(command)
                color = 0x0000FF
            except CommandNotFoundException as e:
                title = "Erreur"
                description = e
                color = 0xFF0000
        else:
            title = "Liste des commandes"
            description = """- help\n- epicgames_set_channel\n- epicgames_set_role"""
            color = 0x0000FF

        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @help.error
    async def help_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("une erreur est survenue")
        print("|ERROR| ", error)


async def setup(bot):
    await bot.add_cog(Help(bot))
