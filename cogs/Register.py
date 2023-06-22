import discord
from discord.ext import commands
import requests
import asyncio
import json
from helpers import checks, create_decoders as decoder, helpers, talkies
import keys

class TFT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.headers = keys.headers
    
    @commands.hybrid_command()
    @commands.check(checks.check_if_bot)
    async def register(self, ctx, region_code, summoner_name):
        """
        Enregiste un nouveau joueur dans la base de données de tracking du bot.
        """
        try:
            region_route = decoder.region[region_code.upper()]
        except Exception as e:
            print("Erreur lors récupération du code région: ", e)
        try:
            APIlink = f"https://{region_route}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{summoner_name}"
            summoner_data = requests.get(APIlink, headers=self.headers)
            summoner_id = summoner_data.json().get("id")
            summoner_name = summoner_data.json().get("name")
            try:
                with open('summoners.json', 'r') as f:
                    summoners = json.load(f)
            except FileNotFoundError:
                print("Le fichier contenant les joueurs n'a pas pu être chargé, tentative de création de celui-ci.")
                try:
                    with open('summoners.json', 'x') as f:
                        summoners = json.load(f)
                except FileNotFoundError:
                    print("Le fichier n'a pas pu être créé, vérifiez que vous avez les droits d'écriture dans le répertoire source.")
            if summoner_id not in summoners:
                summoners[summoner_id] = summoner_name
                with open('summoners.json', 'w') as f:
                    json.dump(summoners, f)
                await ctx.send(f"Le joueur {summoner_name} a bien été enregistré.")
            else:
                await ctx.send(f"Le joueur {summoner_name} est déjà enregistré.")
        except requests.exceptions.RequestException as e:
            print("Erreur lors de la requête pour récupérer le rang du joueur: ", e)