import discord
from discord import ui
from discord.ext import commands
import toml
import os
import datetime
from app.classes.Logger import Logger as Logger
from cogs.Support import SupportPanelView , TicketView
import pymysql

class Bot(commands.Bot):
    def __init__(self , logger)-> None:
        super().__init__(command_prefix="/" , intents=discord.Intents.all())
        self.cogslist = []
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.cogslist.append(filename[:-3])
    
    
    async def on_ready(self)-> None:
        await self.change_presence(status=discord.Status.online , activity=discord.Activity(name = "The Wonderland" , type = discord.ActivityType.watching , state ="Madness incoming..."))
        logger.log(state = "info" , message= f"Logged as {self.user.name}")
        synced = await self.tree.sync()
        logger.log(state="info" , message=  f'Synced commands: {len(synced)}')
    
    async def setup_hook(self) -> None:
        for cog in self.cogslist:
            try:
                await self.load_extension(f"cogs.{cog}")
                logger.log(state="info" , message=  f'{cog} extension is loaded')
            except Exception as e:
                logger.log(state="error" , message=  f"{cog} extension can't be loaded -> {e}")
        with open('app/default.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            connection = pymysql.connect(host=config['database']['adress'],user=config['database']['user'],password=config['database']['password'],database=config['database']['name'],cursorclass=pymysql.cursors.DictCursor)
            with connection:
                with connection.cursor() as cursor:
                    sql = "SELECT panel_id FROM support"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result != None:
                        for panel in result:
                            self.add_view(SupportPanelView(), message_id=panel["panel_id"])
                    sql = "SELECT ticket_id , is_closed FROM ticket"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result != None:
                        for ticket in result:
                            if ticket['is_closed'] == False:
                                self.add_view( TicketView(), message_id=ticket["ticket_id"])
        return await super().setup_hook()



logger = Logger()
bot = Bot(logger)

with open('app/default.toml','r', encoding="utf8") as f:
    config = toml.load(f)
                     


if __name__ == "__main__":

    bot.run(config['connect']['token'])