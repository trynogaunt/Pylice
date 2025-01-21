import os
import discord
from discord.ext import commands
from discord import app_commands
import toml

MY_GUILD = discord.Object(id=1218400838196662403)
class Pylice(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents.default())
        print(f"{self.__class__.__name__} is running...")
        
    
    async def setup_hook(self):
        for cog in os.listdir("app/cogs"):
            if cog.endswith(".py") and not cog.startswith("__"):
                try:
                    await self.load_extension(f"app.cogs.{cog[:-3]}")
                    print(f"{cog} is loaded.")
                except Exception as e:
                    print(f"Failed to load {cog}.")
                    print(e)

        
        await self.tree.sync(guild=MY_GUILD)
        print(f"Command tree is ready.")

    async def on_ready(self):
        for command in self.tree.get_commands():
            print(f"Command: {command.name}")
        print(f"{self.user} is ready.")

client = Pylice()  
if __name__ == "__main__":
    with open("app/core.toml") as f:
        config = toml.load(f)
        client.run(config['client']["token"])