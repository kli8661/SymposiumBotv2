# Kent Reddit Bot

import praw
import random
import discord
import requests
from bs4 import BeautifulSoup
from prawcore import NotFound
from discord.ext import commands
from discord.ext.commands import Bot

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D2f2UA.AFTB7ougi3e3U0vytq7wUZ8RPIw'
BOT_PREFIX = '.'
client = Bot(command_prefix=BOT_PREFIX)
reddit = praw.Reddit(client_id='35201Cc7I7xVlA',
                     client_secret='ARuwXMrYhEZTjxq9UZlkIHOiL10',
                     user_agent='praw_bot')


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
        msg = 'You can use this every 5 seconds, please try again in {:.2f}s'.format(error.retry_after)
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@hot_posts.error
async def value_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        msg = 'Use a number from 1-25.'
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@hot_posts.error
@rsearch.error
async def missing_argument_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        msg = 'Put something in please.'
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


@client.command(name='r_meme',
                description='Grab memes from subreddits.',
                brief='Grabs memes.',
                pass_context=True)
async def r_meme(ctx):
    channel = ctx.message.channel
    subredditlist = ['dankmemes', 'memes', 'deepfriedmemes', 'nukedmemes',
                     'surrealmemes', 'wholesomememes', 'comedycemetery']
    sub = random.choice(subredditlist)
    post_sub = reddit.subreddit(sub)
    posts = [post for post in post_sub.hot(limit=20)]
    random_post_number = random.randint(0, 20)
    random_post = posts[random_post_number]
    url = random_post.url
    img_extension = ('jpg', 'jpeg', 'png', 'gif')
    if url.endswith(img_extension):
        yield url
    elif 'imgur' in url and ('/a/' in url or '/gallery/' in url):
        r = requests.get(url).text
        soup_ob = BeautifulSoup(r, 'html.parser')
        for link in soup_ob.find_all('div', {'class': 'post-image'}):
            try:
                partial_link = link.img.get('src')
                url = 'https:' + partial_link
                yield url
            except:
                pass
    else:
        raw_url = url + '.jpg'
        try:
            r = requests.get(raw_url)
            r.raise_for_status()
            extension = r.headers['content-type'].split('/')[-1]
        except Exception as e:
            extension = ''
        if extension in img_extension:
            link = '{url}.{ext}'.format(url=url, ext=extension)
            yield link

    image = link
    print(image)
    await client.send_message(channel, link)

client.run(TOKEN)
