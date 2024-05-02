from typing import List
import discord
from discord.ext import commands
from discord import ui
from discord import app_commands
from discord.utils import MISSING
from app.classes.Database import Connexion as cxn
from app.classes.Language import Language
import pymysql
import toml
import datetime
import asyncio
from app.classes.Language import Language
import random

class Test(commands.Cog):
    def __init__(self , bot = commands.Bot) -> None:
        self.int = random.random()
        super().__init__()

    @app_commands.command()
    async def random(self, interaction : discord.Interaction):
        await interaction.response.send_message(self.int)
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Test(bot) , guild=discord.Object(id=1218400838196662403))