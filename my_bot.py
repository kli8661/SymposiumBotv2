import discord
import testing as ts
import reddit as rd
import music as mu

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

client = discord.Client()


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

ts.on_ready()
ts.list_servers()
mu.join()
mu.leave()
ts.ping()
ts.eight_ball()
ts.square()
ts.bitcoin()
ts.help_me()
ts.clear()
rd.rimage()


client.run(TOKEN)
