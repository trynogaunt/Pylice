from typing import List
import discord
from discord.ext import commands
from discord import ui
from discord import app_commands
from discord.utils import MISSING
from app.classes.Database import Connexion as cxn
import pymysql
import toml
import datetime
import asyncio

class TicketModal(discord.ui.Modal, title='Support Ticket'):
    modal_title = discord.ui.TextInput(label="Title", style=discord.TextStyle.short, placeholder="Ticket Title" ,required=True)
    problem = discord.ui.TextInput(label="Describe your problem", style=discord.TextStyle.long , placeholder="My problem is...", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        title = f"⏲️ {self.modal_title.value}"
        thread = await interaction.channel.create_thread(name=title, type=discord.ChannelType.private_thread)
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d")
        await thread.add_user(interaction.user)
        ticket = await thread.send(f"From: **{interaction.user.name}**\n\nDate: **{date}**\n\nIssue:\n```{self.problem.value}```", view=TicketView())
        with open('app/default.toml','r', encoding="utf8") as f:
             config = toml.load(f)
             connection = pymysql.connect(host=config['database']['adress'],user=config['database']['user'],password=config['database']['password'],database=config['database']['name'],cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO ticket VALUES (%s, %s , %s)"
                cursor.execute(sql , (interaction.guild.id , ticket.id , False))
                connection.commit()
        await interaction.response.send_message(f"Ton ticket a été créé ici: {thread.mention}", ephemeral=True)
    
class TicketDropdown(discord.ui.Select):
    def __init__(self) -> None:
        options = [
            discord.SelectOption(label='Waiting', description='Ticket en attente du staff', emoji='⏲️'),
            discord.SelectOption(label='Resolved', description='Ticket résolu et fermé', emoji='✅'),
            discord.SelectOption(label='Opened', description='Ticket en cours de résolution', emoji='❓')
        ]
        super().__init__(custom_id="ticket_dropdown", options=options)
    

    async def callback(self, interaction: discord.Interaction):
        closed = False
        match self.values[0]:
            case "Waiting":
                msg = "Ticket mis en cours de résolution"
                eph = True
                title = f"⏲️ {interaction.channel.name[2:]}"
            case "Resolved":
                msg = "Ticket fermé"
                eph = False
                title = f"✅ {interaction.channel.name[2:]}"
                closed = True
                with open('app/default.toml','r', encoding="utf8") as f:
                    config = toml.load(f)
                    connection = pymysql.connect(host=config['database']['adress'],user=config['database']['user'],password=config['database']['password'],database=config['database']['name'],cursorclass=pymysql.cursors.DictCursor)
                    with connection:
                        with connection.cursor() as cursor:
                            sql = "UPDATE ticket SET is_closed = %s WHERE ticket_id = %s"
                            cursor.execute(sql , (True , interaction.message.id))
                            connection.commit()
            case "Opened":
                msg = "Ticket en attente de staff"
                eph = True
                title = f"❓ {interaction.channel.name[2:]}"
        await interaction.response.send_message(msg , ephemeral=eph)
        if closed:
            await interaction.channel.edit(name=title, archived=closed)
        

class TicketView(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180):
        super().__init__(timeout=None)
        self.add_item(TicketDropdown())
                
class SupportPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Open support ticket', style=discord.ButtonStyle.green, custom_id='persistent_support_button:green')
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal())
    


class Support(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def support_panel(self , interaction : discord.Interaction , message : str):
        with open('app/default.toml','r', encoding="utf8") as f:
            config = toml.load(f)
            connection = pymysql.connect(host=config['database']['adress'],user=config['database']['user'],password=config['database']['password'],database=config['database']['name'],cursorclass=pymysql.cursors.DictCursor)
            with open('app/language.toml','r', encoding="utf8") as l:
                language_data = toml.load(l)
                with connection:
                    with connection.cursor() as cursor:
                        sql = "SELECT support_channel_id , command_channel_id , server_language FROM `servers` WHERE id = %s"
                        cursor.execute(sql , (interaction.guild.id))
                        result = cursor.fetchone()
                
                if result == None:
                    await interaction.response.send_message(language_data[result['server_language']['server_unregistered']])
                else:
                    channel = interaction.guild.get_channel(result['support_channel_id'])
                    if result['command_channel_id'] == interaction.channel.id:
                        view = SupportPanelView()
                        sql = "SELECT panel_id FROM support"
                        cursor.execute(sql)
                        result  = cursor.fetchone()
                        if result == None:
                            await interaction.response.defer()
                            embed = discord.Embed()
                            embed.add_field(name="Ticket panel", value=message)
                            embed.set_footer(text=self.bot.user.name , icon_url=self.bot.user.avatar.url)
                            embed.colour = discord.Colour.brand_green()
                            panel = await channel.send(embed=embed, view=view)
                            sql = "INSERT INTO support VALUES (%s, %s)"
                            cursor.execute(sql , (interaction.guild.id , panel.id))
                            connection.commit()
                            await panel.pin()
                            await interaction.followup.send(language_data[result['server_language']['support_panel_created']])
                        else:
                            await interaction.response.send_message("Votre panel existe déjà" , ephemeral=True)
                    else:
                        await interaction.response.send_message("Ceci n'est pas un channel de commande" , ephemeral=True)

        


                
        


async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Support(bot))