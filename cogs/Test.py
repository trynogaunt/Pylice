import discord
from discord.ext import commands
from discord import ui
from discord import app_commands

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
    
    
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Test(bot), guild=discord.Object(id=1218400838196662403))