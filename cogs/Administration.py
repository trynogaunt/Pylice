import discord
from discord.ext import commands
from discord import ui
from discord import app_commands
from app.classes.Database import Connexion as cxn
import pymysql
import toml


class Administration(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()

    @app_commands.command(description="Purge all unpinned message")
    async def purge(self, interaction : discord.Interaction):
        def not_pinned(m):
            return not m.pinned
        purged = await interaction.channel.purge(limit=100, check=not_pinned)
        await interaction.channel.send(f"{len(purged)} messages supprimés (Ce message s'auto-détruira 10 secondes après son envoi)", delete_after=10)


async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Administration(bot), guild=discord.Object(id=1218400838196662403))