import discord
from testing import *
from reddit import *
from google import *
from music import *
from discord.ext.commands import Bot

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'
BOT_PREFIX = '.'
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

on_ready()
list_servers()
join()
leave()
ping()
eight_ball()
square()
bitcoin()
help_me()
clear()
rimage()


client.run(TOKEN)
