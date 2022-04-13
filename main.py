import json
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, CommandNotFound
from discord.ext.commands.core import command
import discord
import requests
from colorama import init, Fore, Back, Style
import os
import time
import asyncio
import random

class s():
    space = " " * 2
    # SECTION SIGN MARKS (LIGHT)
    sred = Style.BRIGHT + "[" + Fore.RED + " \u00a7 " + Fore.WHITE + "] "
    sblue = Style.BRIGHT + "[" + Fore.BLUE + " \u00a7 " + Fore.WHITE + "] "
    # EXCLAMATION MARKS (LIGHT)
    red = Style.BRIGHT + "[" + Fore.RED + " ! " + Fore.WHITE + "] "
    blue = Style.BRIGHT + "[" + Fore.BLUE + " ! " + Fore.WHITE + "] "
    # QUESTION MARKS (LIGHT)
    qred = Style.BRIGHT + "[" + Fore.RED + " ? " + Fore.WHITE + "] "
    qblue = Style.BRIGHT + "[" + Fore.BLUE + " ? " + Fore.WHITE + "] "
    # EXLAMATION MARKS (DARK)
    dred = Style.BRIGHT + "[" + Style.RESET_ALL + Fore.RED + " ! " + Fore.WHITE + Style.BRIGHT + "] "
    dblue = Style.BRIGHT + "[" + Style.RESET_ALL + Fore.BLUE + " ! " + Fore.WHITE + Style.BRIGHT + "] "
    # QUESTION MARKS (DARK)
    dqred = Style.BRIGHT + "[" + Style.RESET_ALL + Fore.RED + " ? " + Fore.WHITE + Style.BRIGHT + "] "
    dqblue = Style.BRIGHT + "[" + Style.RESET_ALL + Fore.BLUE + " ? " + Fore.WHITE + Style.BRIGHT + "] "
    # SECTION SIGN MARKS (DARK)
    dsred = Style.BRIGHT + "[" + Style.RESET_ALL + Fore.RED + " \u00a7 " + Fore.WHITE + Style.BRIGHT + "] "
    dsblue = Style.BRIGHT + "[" + Style.RESET_ALL + Fore.BLUE + " \u00a7 " + Fore.WHITE + Style.BRIGHT + "] "

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
prefix = config.prefix

# Load selfbot
os.system('cls')
print("\n\n\n\n\n")
print(s.dsred + Style.BRIGHT + "Loading selfbot...")
bot = Bot(config.prefix, help_command=None, self_bot=True)

time.sleep(1)
print("\n\n\n\n\n")
print(f'''        {Fore.BLUE}╔════════════════════════════════════════════════╗
        {Fore.BLUE}║ ██╗  ██╗███████╗███╗   ██╗██████╗ ██╗ ██████╗  ║
        {Fore.BLUE}║ ╚██╗██╔╝██╔════╝████╗  ██║██╔══██╗██║██╔═══██╗ ║
        {Fore.BLUE}║  ╚███╔╝ █████╗  ██╔██╗ ██║██████╔╝██║██║   ██║ ║
        {Fore.BLUE}║  ██╔██╗ ██╔══╝  ██║╚██╗██║██╔══██╗██║██║   ██║ ║
        {Fore.BLUE}║ ██╔╝ ██╗███████╗██║ ╚████║██║  ██║██║╚██████╔╝ ║
        {Fore.BLUE}║ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝ ╚═════╝  ║
        {Fore.BLUE}╚════════════════════════════════════════════════╝
        {Fore.RESET}Xenrio's prefix: {Fore.BLUE}{config.prefix}{Fore.RESET}, for help type {Fore.BLUE}{config.prefix}commands{Fore.RESET}
''' + Fore.RESET)


@bot.event
async def on_ready():
    bot.remove_command("help")
    activity = discord.Game(name="Fortnite Battle Pass", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print(s.dsblue + " Logged in as " + Fore.YELLOW + bot.user.name + "#" + bot.user.discriminator + Fore.WHITE + Style.BRIGHT)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        c = ctx.message.content.split(' ')[0].replace(config.prefix, "")
        print(s.dred + f"Command not found: {c}")
        return
    raise error

@bot.command(usage='<text>')
async def btc(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    await ctx.send(content="> Bitcoin\n>   ╠ USD: $" + str(usd) + "\n>   ╚ EUR: €" + str(eur), delete_after=config.delete_after)

@bot.command(usage='<text>')
async def eth(ctx):
    await ctx.message.delete()
    r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR')
    r = r.json()
    usd = r['USD']
    eur = r['EUR']
    await ctx.send(content="> Etherium\n>   ╠ USD: $" + str(usd) + "\n>   ╚ EUR: €" + str(eur), delete_after=config.delete_after)

@bot.command()
async def commands(ctx):
    await ctx.message.delete()
    text = "Commands:\n"
    for command in bot.commands:
        text += "`" + command.name + "`, "
    await ctx.send(content=text, delete_after=config.delete_after)

@bot.command()
async def info(ctx, command: str = None):
    await ctx.message.delete()
    if command is None:
        text = "Info:\n"
        for command in bot.commands:
            text += "`" + command.name + "`, "
        await ctx.send(content=text, delete_after=config.delete_after)
    else:
        command = bot.get_command(command)
        if command is None:
            await ctx.send(content="Command not found", delete_after=config.delete_after)
        else:
            text = "Info:\n"
            text += "`" + command.name + "`\n"
            text += "Usage: " + command.usage + "\n"
            text += "Description: " + command.description + "\n"
            await ctx.send(content=text, delete_after=config.delete_after)

@bot.command(name='passwordgen', description='Generate a password')
async def passwordgen(ctx, length: int):
    await ctx.message.delete()
    letters = "ABCDEFGHIJKLMNOPQRSTUVXYZabcdefghijklmnopqrstuvxyz1234567890!@#$%^&*[]:;"
    passw = ''.join(random.choice(letters) for i in range(length))
    await ctx.send("> Password Gen: \n||`{}`||".format(passw), delete_after=15)

@bot.command(name='auto-text', aliases=['text'], description='Auto-text use underscore for spaces', usage='<channelid> <text> <interval> <maxinterval>')
async def _auto_text(ctx, channel: discord.TextChannel, text: str, duration: int, max_duration: int):
    await ctx.message.delete()
    count = 0
    while True:
        try:
            count += 1
            await channel.send(text.replace("_", " "))
            print(s.space+f'{Fore.GREEN}[AUTO-TEXT]{Style.RESET_ALL} {count}x "{text.replace("_", " ")}" sent.'+Fore.RESET)
            await asyncio.sleep(random.randint(duration, max_duration))
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)


bot.run(config.token, bot=False)