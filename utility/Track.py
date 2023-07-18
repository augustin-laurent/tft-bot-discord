import discord
from discord.ext import commands
import json
import requests
import asyncio
import json
import pickle
import os
from helpers import checks, create_decoders as decoder, helpers, talkies
import keys

class Track():
    def __init__(self, bot):
        self.bot = bot
        self.headers = keys.headers
        self.cache_file = "cache.pickle"

        try:
            if os.path.exists("summoners.json") and os.path.getsize("summoners.json") > 0:
                with open('summoners.json', 'r') as f:
                    self.ranks = json.load(f)
        except FileNotFoundError:
            print("Le fichier contenant les rangs n'a pas pu être chargé, est-il disponible dans le répertoire source ?")

    def get_rank(self, region_code, summonerid):
        """
        Enregistre le rang des joueurs contenu dans sumonners.json dans un fichier cache
        """
        try:
            region_route = decoder.region[region_code.upper()]
        except Exception as e:
            print("Erreur lors récupération du code région: ", e)
        try:
            APIlink = "https://{}.api.riotgames.com/tft/league/v1/entries/by-summoner/{}".format(region_route, summonerid)
            summoner_data = requests.get(APIlink, headers=self.headers)
            return summoner_data[0].get("tier"), summoner_data[0].get("rank"), summoner_data[0].get("summonerName"), summoner_data[0].get("wins"), summoner_data[0].get("losses"), summoner_data[0].get("hotStreak")
        except requests.exceptions.RequestException as e:
            print("Erreur lors de la requête pour récupérer le rang du joueur: ", e)
    
    def store_ranks(self):
        """
        Store ranks of all player in SUMMONERID in a cache file
        """
        previous_ranks = {}
        if os.path.exists(self.cache_file) and os.path.getsize(self.cache_file) > 0:
            try:
                with open(self.cache_file, 'rb') as file:
                    previous_ranks = pickle.load(file)
            except FileNotFoundError:
                print("Le fichier de cache n'a pas pu être trouvé, tentative de création du fichier.")
                try:
                    with open(self.cache_file, 'x') as file:
                        previous_ranks = pickle.load(file)
                except FileNotFoundError:
                    print("Le fichier n'a pas pu être créé, vérifiez que vous avez les droits d'écriture dans le répertoire source.")               
        try:
            with open('summoners.json', 'r') as f:
                summoners = json.load(f)
        except FileNotFoundError:
            print("Le fichier contenant les joueurs n'a pas pu être chargé, est-il disponible dans le répertoire source ?")
        for summoner_id in summoners:
            information_player = list(self.get_rank(summoner_id))
            current_rank = information_player[0] + " " + information_player[1]
            if summoner_id not in previous_ranks:
                previous_ranks[information_player[2]] = current_rank
        try:
            with open(self.cache_file, 'wb') as file:
                print(previous_ranks)
                pickle.dump(previous_ranks, file)
        except Exception as e:
            print(f":Impossible d'écrire les informations dans le fichier de cache {e}")

    async def check_rank_changes(self):
        try:
            with open(self.cache_file, 'rb') as file:
                previous_ranks = pickle.load(file)
        except FileNotFoundError:
            print("Cache file not found. Please run the bot once to create the cache file.")
        while True:
            for summoner_id in SUMMONERID:
                information_player = self.get_rank(summoner_id)
                current_rank = information_player[0] + " " + information_player[1]
                previous_rank = previous_ranks[information_player[2]]
                if current_rank != previous_rank:
                    if previous_rank != "":
                        current_rank_value = RANK_DICTIONNARY[current_rank.split(" ")[0].lower()]
                        previous_rank_value = RANK_DICTIONNARY[previous_rank.split(" ")[0].lower()]
                        if current_rank_value < previous_rank_value:
                            message = f"{information_player[2]} a dérank cette sale merde, il est passé de {previous_rank} à {current_rank}."
                            await self.send_messages(message)
                        else:
                            message = f"{information_player[2]} a rank up ce gros beau gosse, il est passé de {previous_rank} à {current_rank}."
                            await self.send_messages(message)
                    previous_ranks[summoner_id] = current_rank
            await asyncio.sleep(60)