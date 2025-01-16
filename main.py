import os
import discord
from discord.ext import commands
from discord import app_commands
import toml

class Pylice(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"{self.__class__.__name__} is running...")
        
        #self.tree = app_commands.CommandTree(self)
        self.status = discord.Status.online
        self.activity = discord.Game(name="working progress...", type=discord.ActivityType.playing, platform="PC")
        self.initial_extensions = [f"app.cogs.{filename[:-3]}" for filename in os.listdir("app/cogs") if filename.endswith(".py")]

    async def setup_hook(self):
        for extension in self.initial_extensions:
            synced = await self.load_extension(extension)
            if synced:
                print("Loaded extension:", extension)
        #self.tree.copy_global_to(guild=discord.Object(id=1218400838196662403))
        #synced = await self.tree.sync(guild=discord.Object(id=1218400838196662403))
        #print(f"Synced {synced}")
        print("Setup command complete")
    
    async def on_ready(self):
        await self.change_presence(status=self.status, activity=self.activity)
        print(f'Logged in as {self.user}')
        print(f'------------------------')

        
intent = discord.Intents.default()
client = Pylice(command_prefix = "/" , intents=intent)



@client.tree.command(name="ping", description="Ping the user who send the command")
async def ping(interaction : discord.Interaction):
    """Ping the user who send the command"""
    await interaction.response.send_message(f"Pong! {interaction.user.mention}: {round(client.latency * 1000)}ms")

if __name__ == "__main__":
    with open("app/core.toml") as f:
        config = toml.load(f)
        client.run(config['client']["token"])