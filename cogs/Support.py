import discord
from discord.ext import commands
from discord import ui
from discord import app_commands
from app.classes.Database import Connexion as cxn
import pymysql
import toml

class TicketModal(discord.ui.Modal, title='Support Ticket'):
    problem = discord.ui.TextInput(label="Describe your problem", style=discord.TextStyle.long , placeholder="My problem is...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        thread = await interaction.channel.create_thread(name=f"{interaction.user.name}'s ticket" , type=discord.ChannelType.private_thread)
        await thread.add_user(interaction.user)
        await thread.send(self.problem.value)
        await interaction.response.send_message("Ca roule")        
class SupportPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Open support ticket', style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal())
    
    @discord.ui.


class Support(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def support_panel(self , interaction : discord.Interaction):
        with open('app/default.toml','r', encoding="utf8") as f:
             config = toml.load(f)
             connection = pymysql.connect(host=config['database']['adress'],user=config['database']['user'],password=config['database']['password'],database=config['database']['name'],cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT support_channel_id , command_channel_id FROM `servers` WHERE id = %s"
                cursor.execute(sql , (interaction.guild.id))
                result = cursor.fetchone()
                
                if result == None:
                    msg = "Votre serveur n'est pas configuré , merci d'utiliser la commande /setup pour commencer la configuration"
                else:
                    if result['command_channel_id'] == interaction.channel.id:
                        view = SupportPanelView()
                        await interaction.channel.send(view=view)
                
        


async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Support(bot), guild=discord.Object(id=1218400838196662403))