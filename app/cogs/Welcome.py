import discord
from discord.ext import commands
from discord import app_commands

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.last_member = None

    @commands.command(name="welcome", description="Welcome a user to the server")
    async def welcome(self, interaction : discord.Interaction):
        """Welcome a user to the server"""
        await interaction.response.send_message(f"Welcome to the server {interaction.user.mention}!")
        print(f"{interaction.user} has joined the server!")
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send(f"Welcome to the server {member.mention}!")
        print(f"{member} has joined the server!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server!")

async def setup(client):
    await client.add_cog(Welcome(client), guild=discord.Object(id=1218400838196662403))