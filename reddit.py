# Kent Reddit Bot

import discord
import praw
from discord.ext.commands import Bot

# urlprefix = "https://reddit.com/r/"
# urlsuffix = "/random.json"
# count = 0

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'
BOT_PREFIX = '.'
client = Bot(command_prefix=BOT_PREFIX)
reddit = praw.Reddit(client_id='y4QgcvDtchCuoA',
                     client_secret='VQrBWpVzb09X1v-W5Bgh62bYoOU',
                     user_agent='prawtutorialv1')


@client.command(name='top_posts',
                description='Grabs the top posts from a subreddit of the users choice.',
                brief='Grabs top posts.',
                alias=['tpost'],
                pass_context=True)
async def top_posts(post):
    post_sub = reddit.subreddit(post)
    hot_posts = post_sub.hot()
    for submission in hot_posts:
        if not submission.stickied:
            embed = discord.Embed(
                title="Top Posts of " + post,
                colour=discord.Colour.blue()
            )

            embed.set_author(name='Hot Posts In: ' + post)
            embed.add_field(name=submission.title, value='Upvotes: ' +
                            submission.ups + ', ' + 'Downvotes: ' + submission.downs, inline=False)

            await client.say(embed=embed)


# @client.command(name='rimage',
#                 description="Grabs image from user subreddit.",
#                 brief="Grabs image from subreddit.",
#                 pass_context=True)
# async def rimage(sub):
#     while True:
#         subreddit = sub.content[7:]
#         subtest = urlprefix + subreddit + '.json'
#         response = http.request('GET', subtest)
#         check = response.data
#         parse = json.loads(check)
#         if parse['data']['dist'] == 0:
#             await client.send_message(sub.channel, 'That subreddit does not exist!')
#             return
#         url = urlprefix + subreddit + urlsuffix
#         while True:
#             response = http.request('GET', url)
#             jsonparse = json.loads(response.data.decode('utf-8'))
#             image = jsonparse[0]['data']['children'][0]['data']['url']
#             if image.endswith('.png') or image.endswith('jpeg') or image.endswith('jpg') or image.endswith('gif'):
#                 await client.send_message(sub.channel, image)
#                 return
#             else:
#                 global count
#                 count += 1
#             if count == 10:
#                 await client.send_message(sub.channel, 'No image found.')
#                 return
#           await client.send_message(sub.channel, 'Try command !rimage subreddit')
#            return


client.run(TOKEN)
