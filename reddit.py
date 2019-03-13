# Kent Reddit Bot

import discord
import praw
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
async def hot_posts(ctx, subreddit, amount):
    subreddit = subreddit
    limit = int(amount)
    channel = ctx.message.channel
    post_sub = reddit.subreddit(subreddit)
    hot = post_sub.hot(limit=limit)
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
                brief='Searches reddit. \n[.rsearch <example_search>]',
                pass_context=True)
async def rsearch(ctx, query):
    channel = ctx.message.channel
    querystr = str(query).replace("_", " ")
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


client.run(TOKEN)
