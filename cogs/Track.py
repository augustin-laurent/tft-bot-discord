import discord
from discord.ext import commands
import requests
import asyncio
import json
from helpers import checks, create_decoders as decoder, helpers, talkies
import keys

RANK_DICTIONNARY = {
    "challenger": 1,
    "grandmaster": 2,
    "master": 3,
    "diamond i": 4,
    "diamond ii": 5,
    "diamond iii": 6,
    "diamond iv": 7,
    "platinum i": 8,
    "platinum ii": 9,
    "platinum iii": 10,
    "platinum iv": 11,
    "gold i": 12,
    "gold ii": 13,
    "gold iii": 14,
    "gold iv": 15,
    "silver i": 16,
    "silver ii": 17,
    "silver iii": 18,
    "silver iv": 19,
    "bronze i": 20,
    "bronze ii": 21,
    "bronze iii": 22,
    "bronze iv": 23,
    "iron i": 24,
    "iron ii": 25,
    "iron iii": 26,
    "iron iv": 27
}

class Track(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.check(checks.check_if_bot)
    async def tftrank(self, ctx, region_code=None, *, summoner=None):
        """Prints the requested players' TFT rank to Discord"""
        print("TFTRANK / {} / {} / {}".format(str(summoner), str(region_code), ctx.author))
        if (region_code == None) or (summoner == None):
            info_msg = "Command format should be: //tftrank [region code] [summoner]\n Use //regions to see list " \
                       "of correct region codes. "
            embed_msg = discord.Embed(
                colour=discord.Colour.red()
            )
            embed_msg.add_field(name="Incorrect command format!", value=info_msg)
        else:
            embed_msg = self.get_player_tft_rank(region_code, summoner)
        await ctx.channel.send(embed=embed_msg)
