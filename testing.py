# Here are some general/testing methods that were worked on by all of us.

import re
import praw
import random
import asyncio
import aiohttp
import json
import discord
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from prawcore import NotFound

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D2f2UA.AFTB7ougi3e3U0vytq7wUZ8RPIw'
BOT_PREFIX = '.'
client = Bot(command_prefix=BOT_PREFIX)

reddit = praw.Reddit(client_id='35201Cc7I7xVlA',
                     client_secret='ARuwXMrYhEZTjxq9UZlkIHOiL10',
                     user_agent='praw_bot')


@client.event
async def on_ready():
    await client.change_presence(game=Game(name=" .help"))
    print("Logged in as " + client.user.name)


@client.command(name='ping',
                description="Tests if the bot is alive.",
                brief="Ping and Pong.")
async def ping():
    await client.say("pong")


@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond. \n[.8ball <question>]",
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
        'Try asking a better question',
        'Certainly',
        'Of Course'
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command(name='clear',
                description='Clears the amount of lines in the text channel the user wants.',
                brief='Clears a certain amount of messages. \n[.clear <amount>]',
                pass_context=True)
async def clear(context, amount):
    amount = amount
    channel = context.message.channel
    lines = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        lines.append(message)
    await client.delete_messages(lines)
    await client.say('Cleared ' + amount + ' messages!')


@client.command(name='square',
                description="Squares a number.",
                brief="Squares a number. \n[.square <number>]")
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

# Fix this later


@client.command(name='help_me',
                description="Help but it sends a private message to you.",
                brief="Private Help.",
                aliases=['helpp', 'help_private'],
                pass_context=True)
async def help_me(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )

    embed.set_author(name='Help')
    embed.add_field(name='.ping', value='Returns Pong!', inline=False)

    await client.send_message(author, embed=embed)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


@client.command(name='join',
                description="Joins current voice channel.",
                brief="Joins voice channel."
                , pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(name='leave',
                description="Leaves voice channel.",
                brief="Leaves voice channel."
                , pass_context=True)
async def leave(ctx):
    vc = await client.join_voice_channel(ctx.message.author.voice_channel)
    await vc.disconnect()


@client.command(name='hot_posts',
                description='Grabs the hot posts from a subreddit of the users choice.',
                brief='Grabs hot posts from subreddit. \n[.hot_posts <subreddit> <number of posts>]',
                pass_context=True)
@commands.cooldown(1.0, 10.0, commands.BucketType.user)
async def hot_posts(ctx, subreddit, amount):
    channel = ctx.message.channel
    if sub_exists(subreddit):
        subreddit = subreddit
    else:
        await client.send_message(channel, "This subreddit doesn't exist!")
    limit = int(amount)
    post_sub = reddit.subreddit(subreddit)
    hot = post_sub.hot(limit=limit + 2)
    embed = discord.Embed(
        author=subreddit,
        title='Top Posts',
        colour=discord.Colour.blue()
    )

    for submission in hot:
        if not submission.stickied:
            ratio = submission.upvote_ratio
            upvote = round((ratio * submission.score)/(2 * ratio - 1)) if ratio != 0.5 else round(submission.score/2)
            downvote = upvote - submission.score
            embed.add_field(name=str(submission.title), value='URL: ' + str(submission.url) + '\n' + 'Upvotes: ' +
                            str(submission.ups) + ', ' + 'Downvotes: ' + str(downvote), inline=False)

    await client.send_message(channel, embed=embed)


@client.command(name='rsearch',
                description='Searches reddit. Replace space with _.',
                brief='Searches reddit. \n[.rsearch <example search>]',
                pass_context=True)
@commands.cooldown(1.0, 10.0, commands.BucketType.user)
async def rsearch(ctx, *, query):
    channel = ctx.message.channel
    querystr = str(query)
    print(querystr)
    sub = reddit.subreddit('all')
    embed = discord.Embed(
        author=querystr,
        title='Search Results For: ' + querystr,
        colour=discord.Colour.blue()
    )
    for i in sub.search(querystr, limit=5):
        embed.add_field(name=str(i.title), value='URL: ' + str(i.url), inline=False)

    await client.send_message(channel, embed=embed)


@rsearch.error
@hot_posts.error
async def timeout_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You can use this every 10 seconds, please try again in {:.2f}s'.format(error.retry_after)
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        await client.send_message(ctx.message.channel, 'Cannot find this command!')
    else:
        raise error


@hot_posts.error
async def value_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        msg = 'Use a number from 1-25.'
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, include_nsfw=True, exact=True)
    except NotFound:
        exists = False
    return exists


client.loop.create_task(list_servers())
client.run(TOKEN)
