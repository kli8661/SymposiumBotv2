# Kent Reddit Bot

import discord
import praw
from discord.ext.commands import Bot

# urlprefix = "https://reddit.com/r/"
# urlsuffix = "/random.json"
# count = 0

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D2f2UA.AFTB7ougi3e3U0vytq7wUZ8RPIw'
BOT_PREFIX = '.'
client = Bot(command_prefix=BOT_PREFIX)
reddit = praw.Reddit(client_id='y4QgcvDtchCuoA',
                     client_secret='VQrBWpVzb09X1v-W5Bgh62bYoOU',
                     user_agent='prawtutorialv1')


@client.command(name='hot_posts',
                description='Grabs the hot posts from a subreddit of the users choice.',
                brief='Grabs hot posts from subreddit.',
                pass_context=True)
async def hot_posts(ctx, subreddit):
    subreddit = subreddit
    channel = ctx.message.channel
    post_sub = reddit.subreddit(subreddit)
    hot = post_sub.hot(limit=12)
    embed = discord.Embed(
        author=subreddit,
        title='Top Posts',
        colour=discord.Colour.blue()
    )

    for submission in hot:
        if not submission.stickied:
            embed.add_field(name=str(submission.title), value='URL: ' + str(submission.url) + '\n' + 'Upvotes: ' +
                            str(submission.ups) + ', ' + 'Downvotes: ' + str(submission.downs), inline=False)

    await client.send_message(channel, embed=embed)

client.run(TOKEN)
