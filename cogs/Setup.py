from typing import List
import discord
from discord import app_commands
from discord import ui
from discord.ext import commands
from discord.utils import MISSING
import toml
import os

class SetupSelect(discord.ui.Select):
    def __init__(self, options) -> None:

        super().__init__(options=options)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        return await interaction.response.send_message(f"{self.values}")


class SetupView(discord.ui.View):
    def __init__(self, options):
        super().__init__(timeout=None)

        self.add_item(SetupSelect(options))
        self.add_item(SetupSelect(options))


class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="setup" , description="First step to use the bot")
    async def setup(self, interaction : discord.Interaction):
        options = []
        for channel in interaction.guild.channels:
            print(channel.type)
            if str(channel.type) == "text":
                options.append(discord.SelectOption(label = f"{channel.name}" , value = channel.id))

        return await interaction.response.send_message(view=SetupView(options))
        
    
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Setup(bot),  guild=discord.Object(id=1218400838196662403))