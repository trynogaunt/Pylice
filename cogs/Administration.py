import discord
from discord.ext import commands
from discord import ui
from discord import app_commands
from app.classes.Database import Connexion as cxn
import pymysql
import toml


class Administration(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
    @app_commands.command(description="Purge all unpinned message")
    @app_commands.checks.has_permissions(manage_messages = True)
    async def purge(self, interaction : discord.Interaction , limit : int = 100):
        await interaction.response.defer()
        def not_pinned(m):
            return not m.pinned
        purged = await interaction.channel.purge(limit=limit, check=not_pinned)
        await interaction.followup.send(f"{len(purged)} messages supprimés (Ce message s'auto-détruira 10 secondes après son envoi)" , ephemeral=True)
    
    @app_commands.command(description="Purge all messages pinned included")
    @app_commands.checks.has_permissions(manage_messages = True)
    async def purge_all(self, interaction : discord.Interaction , limit : int =100):
        await interaction.response.defer()
        purged = await interaction.channel.purge(limit=limit)
        await interaction.followup.send(f"{len(purged)} messages supprimés (Ce message s'auto-détruira 10 secondes après son envoi)", ephemeral=True)
    
    @commands.Cog.listener()
    async def on_member_join(self , member :  discord.Member):
        with open('app/default.toml','r', encoding="utf8") as f:
             config = toml.load(f)
             connection = pymysql.connect(host=config['database']['adress'],user=config['database']['user'],password=config['database']['password'],database=config['database']['name'],cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT welcome_channel_id FROM `servers` WHERE id = %s"
                cursor.execute(sql , (member.guild.id))
                result = cursor.fetchone()
                channel_id  = result['welcome_channel_id']
                embed = discord.Embed()
                embed.set_author(name=member.name , icon_url=member.avatar.url)
                embed.add_field(name="", value=f"Bienvenue" , inline=True)
                await member.guild.get_channel(channel_id).send(embed=embed)


async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Administration(bot), guild=discord.Object(id=1218400838196662403))