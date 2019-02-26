import discord
import testing as ts
# import google as gl
# import music as mu
# import reddit as rd

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
ts.help_private()

client.run(TOKEN)
