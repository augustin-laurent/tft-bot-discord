import discord
from discord.ext import commands
from discord import app_commands
from helpers import checks


class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.check(checks.check_if_bot)
    async def ping(self, ctx):
        await ctx.send('pong!')

    @commands.hybrid_command()
    @commands.check(checks.check_if_bot)
    async def helpme(self, ctx):
        msg = "\n**//recentmatch** *[region] [summoner]* - Renvoie le match TFT le plus récent pour le joueur spécifié.`\n\
    **//matchhistory** *[region] [summoner]* - Renvoie une liste de match TFT pour le joueur spécifié. Ajoute une réaction pour avoir les détails d'un match!\n\
    **//tftrank** *[region] [summoner]* - Renvoie le rang pour le joueur spécifié.\n\
    **//register** *[region] [summoner]* - Enregistre le joueur dans un fichier pour faire un tracking des rangs en permanance.\n\
    **//regions** - Renvoie une liste de code de région.\n\
    **//ping** - Renvoie pong.\n"
    
        embed_msg = discord.Embed(
            colour=discord.Colour.green()
        )
        embed_msg.add_field(name="Liste des commandes", value=msg, inline=False)

        await(ctx.channel.send(embed=embed_msg))

async def setup(bot):
    await bot.add_cog(Basic(bot))
