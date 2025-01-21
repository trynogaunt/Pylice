import sys
import os
import discord
from discord.ext import commands
from discord import app_commands

sys.path.append('C:/Users/tryno/Desktop/Pylice/app/')

from views.voiceSetupView import VoiceSetupView

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping(self, interaction):
        await interaction.response.send_message(f"Pong! {round(self.client.latency * 1000)}ms pd", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog {__class__.__name__} is loaded.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            pass
        elif after.channel is not None and after.channel.id == 1320402697039380622:
            pass
            

async def setup(client):
    await client.add_cog(Voice(client))