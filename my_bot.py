import discord
import testing as ts

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

ts.on_ready()
ts.ping()
ts.eight_ball()
ts.square()
ts.bitcoin()
ts.list_servers()
ts.help_me()
ts.join()
ts.leave()
ts.rimage()
ts.clear()

client.run(TOKEN)
