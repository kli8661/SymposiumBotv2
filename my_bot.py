import discord
import testing as ts
# import google as gl
# import music as mu
# import reddit as rd

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

client = discord.Client()
client.remove_command('help')


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return


@client.command(pass_content=True)
async def help(cmd):
    author = cmd.message.author

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )

    embed.set_author(name='Help')
    embed.add_field(name='$ping', value='Returns pong', inline=False)

    await client.send_message(author, embed=embed)

ts.on_ready()
ts.ping()
ts.eight_ball()
ts.square()
ts.bitcoin()
ts.list_servers()

client.run(TOKEN)
