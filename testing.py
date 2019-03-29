# Here are some general/testing methods that were worked on by all of us.

import praw
import random
import asyncio
import aiohttp
import json
import discord
import youtube_dl
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from prawcore import NotFound

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D2f2UA.AFTB7ougi3e3U0vytq7wUZ8RPIw'
BOT_PREFIX = '.'
players = {}
client = Bot(command_prefix=BOT_PREFIX)
notInChannel = True

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
    try:
        squared_value = float(number) * float(number)
        await client.say(str(number) + " squared is " + str(squared_value))
    except ValueError:
        await client.say('Not a number, use .square <number>.')


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
    server = ctx.message.server
    vc = client.voice_client_in(server)
    if client.is_voice_connected(server):
        await vc.move_to(channel)
        await client.say("I joined the voice channel: {}".format(channel))
    else:
        await client.join_voice_channel(channel)
        await client.say("I joined the voice channel: {}".format(channel))


@client.command(name='leave',
                description="Leaves voice channel.",
                brief="Leaves voice channel."
                , pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    vc = client.voice_client_in(server)
    await vc.disconnect()


@client.command(name='play',
                description='Plays music.',
                brief='Plays Music.\n'
                      '[.play <URL>]',
                pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()
    await client.send_message(server, 'Playing Music')


@client.command(name='pause',
                description='Pauses music.',
                brief='Pause Music',
                pass_context=True)
async def pause(ctx):
    try:
        pid = ctx.message.server.id
        players[pid].pause()
        await client.say('Paused')
    except KeyError:
        await client.say('Not in channel / Not playing music.')


@client.command(name='resume',
                description='Resumes music.',
                brief='Resumes Music',
                pass_context=True)
async def resume(ctx):
    try:
        rid = ctx.message.server.id
        players[rid].resume()
        await client.say('Resumed')
    except KeyError:
        await client.say('Not in channel / Not playing music.')


@client.command(name='stop',
                description='Stops music.',
                brief='Stops Music',
                pass_context=True)
async def stop(ctx):
    rid = ctx.message.server.id
    players[rid].stop()
    await client.say('Music Stopped')


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


def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, include_nsfw=True, exact=True)
    except NotFound:
        exists = False
    return exists


@client.command(name='rsearch',
                description='Searches reddit.',
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


@client.command(name='r_meme',
                description='Grabs memes.',
                brief='Grabs memes from meme subreddits.',
                pass_context=True)
@commands.cooldown(1.0, 3.0, commands.BucketType.user)
async def r_meme(ctx):
    channel = ctx.message.channel
    import random
    subredditlist = ['dankmemes', 'memes', 'deepfriedmemes', 'nukedmemes',
                     'surrealmemes', 'wholesomememes', 'comedycemetery', 'me_irl', 'bonehurtingjuice']
    sub = random.choice(subredditlist)
    print(sub)
    post_sub = reddit.subreddit(sub)
    posts = [post for post in post_sub.new(limit=100)]
    random_post_number = random.randint(0, 100)
    random_post = posts[random_post_number]
    url = random_post.url
    print(url)
    if url.endswith('.jpg') | url.endswith('.jpeg') | url.endswith('.png') | url.endswith('gif'):
        if not random_post.stickied:
            await client.send_message(channel, sub + '\n' + url)
    else:
        await r_meme()
        await client.send_message('Unable to find meme, please try again.')


@rsearch.error
@hot_posts.error
async def timeout_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You can use this every 10 seconds, please try again in {:.2f}s'.format(error.retry_after)
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@r_meme.error
async def meme_antispam(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You can use this every 3 seconds, please try again in {:.2f}s'.format(error.retry_after)
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@square.error
@hot_posts.error
@rsearch.error
async def missing_argument_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        msg = 'Missing required argument, use .help for more info.'
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


@leave.error
async def channel_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        await client.send_message(ctx.message.channel, 'Not in channel!')
    else:
        raise error


client.loop.create_task(list_servers())
client.run(TOKEN)
