from typing import List
import discord
from discord import app_commands
from discord import ui
from discord.ext import commands
from discord.utils import MISSING
import toml
import pymysql
import datetime
from app.classes import Logger

class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="setup" , description="First step to use the bot")
    async def setup(self, interaction : discord.Interaction , command_channel : discord.TextChannel , support_channel : discord.TextChannel , welcome_channel : discord.TextChannel) :
        with open('app/default.toml','r', encoding="utf8") as f:
             config = toml.load(f)
             connection = pymysql.connect(host=config['database']['adress'],user=config['database']['user'],password=config['database']['password'],database=config['database']['name'],cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `servers` WHERE id = %s"
                cursor.execute(sql , (interaction.guild.id))
                result = cursor.fetchone()
                if result != None:
                    msg = "Ce serveur est déjà enregistré"
                else:
                    msg = f"Le serveur {interaction.guild.name} est configuré"
                    date = datetime.datetime.now()
                    date = date.strftime("%y-%m-%d %H:%M:%S")
                    sql = "INSERT INTO pylice.servers (id, name, owner , support_channel_id , command_channel_id, welcome_channel_id) VALUES (%s , %s , %s , %s , %s , %s)"
                    print(sql)
                    cursor.execute(sql, (interaction.guild.id , str(interaction.guild.name) , interaction.guild.owner_id , support_channel.id , command_channel.id , welcome_channel.id))
            connection.commit()
                    
        await interaction.response.send_message(msg , ephemeral=True)
        
    
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Setup(bot),  guild=discord.Object(id=1218400838196662403))