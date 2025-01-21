import sys
import os
import discord
from discord.ext import commands
from discord import app_commands
sys.path.append('C:/Users/tryno/Desktop/Pylice/app/')
MY_GUILD = discord.Object(id=1218400838196662403)
class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="setup", description="Setup the bot.")
    async def setup(self, interaction):
        print("test")
        await interaction.response.send_message("Starting setup.")
        for setupfile in os.listdir("app/server_setup"):
            if setupfile.endswith(".toml") and setupfile.startswith(f"{interaction.guild_id}"):
                await interaction.response.send_message("Setup already done.")
            else:
                await interaction.response.send_message("Starting setup.")
                with open(f"app/server_setup/{interaction.guild_id}.toml", "w") as f:
                    f.write("setup = true")
                await interaction.response.send_message("Setup done.")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {__class__.__name__} is loaded.")


async def setup(client):
    await client.add_cog(Setup(client),  guilds = [MY_GUILD])