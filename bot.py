import discord
import keys
from discord.ext import commands, tasks

headers = keys.headers
discord_bot_key = keys.discord_bot_key
intents = discord.Intents.default()
intents.message_content = True

# Run the Discord bot and add cogs
bot  = commands.Bot(command_prefix = '!', intents=intents)
@bot.event
async def on_ready():
    await bot.load_extension("cogs.Basic")
    await bot.load_extension("cogs.Admin")
    await bot.load_extension("cogs.TFT")
    print('Le bot est en ligne en tant que {0.user}'.format(bot))
    # Set the Bot's status message (Listening to //help)
    activity = discord.Activity(name='!help', type=discord.ActivityType.listening)
    await bot.change_presence(activity=activity)

bot.run(discord_bot_key)