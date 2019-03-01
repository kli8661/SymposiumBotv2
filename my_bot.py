import discord
from reddit import rimage
from music import join, leave
from testing import on_ready, ping, eight_ball, square, bitcoin, list_servers, help_me, clear
# import reddit as rd
# import music as mu

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

client = discord.Client()


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
