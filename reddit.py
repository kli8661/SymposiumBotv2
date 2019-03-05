# Kent Reddit Bot

import json
import http
from discord.ext.commands import Bot

urlprefix = "https://reddit.com/r/"
urlsuffix = "/random.json"
count = 0
TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'
BOT_PREFIX = '.'
client = Bot(command_prefix=BOT_PREFIX)


@client.command(name='rimage',
                description="Grabs image from user subreddit.",
                brief="Grabs image from subreddit.",
                pass_context=True)
async def rimage(sub):
    while True:
        subreddit = sub.content[7:]
        subtest = urlprefix + subreddit + '.json'
        response = http.request('GET', subtest)
        check = response.data
        parse = json.loads(check)
        if parse['data']['dist'] == 0:
            await client.send_message(sub.channel, 'That subreddit does not exist!')
            return
        url = urlprefix + subreddit + urlsuffix
        while True:
            response = http.request('GET', url)
            jsonparse = json.loads(response.data.decode('utf-8'))
            image = jsonparse[0]['data']['children'][0]['data']['url']
            if image.endswith('.png') or image.endswith('jpeg') or image.endswith('jpg') or image.endswith('gif'):
                await client.send_message(sub.channel, image)
                return
            else:
                global count
                count += 1
            if count == 10:
                await client.send_message(sub.channel, 'No image found.')
                return
            await client.send_message(sub.channel, 'Try command !rimage subreddit')
            return


client.run(TOKEN)
