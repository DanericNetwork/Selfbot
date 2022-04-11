import json
import discord.ext as commands
from discord.ext.commands import Bot
import discord
from discord_slash.utils.manage_components import ComponentContext, create_actionrow, create_button, create_select, create_select_option
from discord_slash.model import ButtonStyle
import requests

class Dict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Configuration(object):

    @staticmethod
    def __load__(data):
        if type(data) is dict:
            return Configuration.load_dict(data)
        else:
            return data

    @staticmethod
    def load_dict(data: dict):
        result = Dict()
        for key, value in data.items():
            result[key] = Configuration.__load__(value)
        return result

    @staticmethod
    def load_json(path: str):
        with open(path, "r") as f:
            result = Configuration.__load__(json.loads(f.read()))
        return result

config = Configuration.load_json("config.json")

print("[+] Loading Selfbot...")

bot = Bot(config.prefix, self_bot=True)

@bot.event
async def on_ready():
    activity = discord.Game(name="Fortnite Battle Pass", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("[+] Selfbot loaded!")

@bot.command()
async def btc(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    await ctx.send(content="Bitcoin price in USD: $" + str(usd) + "\nBitcoin price in EUR: €" + str(eur), delete_after=config.delete_after)

bot.run(config.token, bot=False)