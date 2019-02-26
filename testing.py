import random
import asyncio
import aiohttp
import json
import discord
from discord import Game
from discord.ext.commands import Bot

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

BOT_PREFIX = '$'

client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name=" $help"))
    print("Logged in as " + client.user.name)


@client.command(name='ping',
                description="Tests if the bot is alive.",
                brief="Ping and Pong.")
async def ping():
    await client.say("pong")


@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'Impossible',
        'Try asking a better question'
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command(name='square',
                description="Squares a number.",
                brief="Squares a number.")
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.command(name='bitcoin',
                description="Check's Bitcoin Price to USD",
                brief="Bitcoin Price.")
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


@client.command(name='help_private',
                description="Help but it sends a private message to you.",
                brief="Private Help.",
                aliases=['helpp'],
                pass_content=True)
async def help_private(cmd):
    author = cmd.message.author

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )

    embed.set_author(name='Help')
    embed.add_field(name='$help_private', value='This Command', inline=False)
    embed.add_field(name='$ping', value='Returns pong', inline=False)
    embed.add_field(name='$eight_ball', value='Returns an answer from beyond', inline=False)
    embed.add_field(name='$square', value='Squares a number', inline=False)
    embed.add_field(name='$bitcoin', value='Checks Bitcoin Prices', inline=False)

    await client.send_message(author, embed=embed)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
