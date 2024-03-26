import discord
from discord.ext import commands
from discord import ui
from discord import app_commands
from app.Database import Connexion as cxn
import pymysql
import toml

class Questionnaire(ui.Modal, title='Questionnaire Response'):
    name = ui.TextInput(label='Name')
    answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)

class Test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self._last_member = None
    
    @app_commands.command(name="testcmd" , description="Send hello for testing")
    async def testcmd(self, interaction : discord.Interaction):
        await interaction.response.send_message("Hello")

    @app_commands.command(name="tesdb" , description="Check db connection")
    async def testdb(self, interaction : discord.Interaction):
        with open('app/default.toml','r', encoding="utf8") as f:
             config = toml.load(f)
             connection = pymysql.connect(host=config['database']['adress'],user=config['database']['user'],password=config['database']['password'],database=config['database']['name'],cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `servers`"
                cursor.execute(sql)
                result = cursor.fetchone()
                await interaction.response.send_message(result['name'])
    
    
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Test(bot), guild=discord.Object(id=1218400838196662403))