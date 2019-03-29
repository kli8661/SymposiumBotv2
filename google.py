import discord
import json
# from discord.ext import commands
from cogs.utils.checks import load_optional_config, embed_perms, get_google_entries
# from cogs.utils.config import get_config_value
import aiohttp
import urllib.parse


TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D2f2UA.AFTB7ougi3e3U0vytq7wUZ8RPIw'
BOT_PREFIX = '.'

m_api_key = 'AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4'
m_cx_key = '008921493878794350931:tioeliy7j1y'


# def google_search(search_term, api_key, cx_id, **kwargs):
   # service = build("customSearch", "v1", developerKey=api_key)
   # res = service.cse().list(q=search_term, cx=cx_id, **kwargs).execute()
 #  return res['items']

 # results = google_search('facebook', api_key, cx_key, num=2)

# for result in results:
   # pprint.pprint(result)

#    title = result['title']
#    link = result['formattedUrl']
#    dis = result['snippet']
#    print(title)
#    print(link)
#    print(dis)

class Google:

    def __init__(self, bot):
        self.bot = bot

        def parse_google_card(self, node):
            if node is None or type(node) is int:
                return None

            e = discord.Embed(colour=0x0057e7)

            calculator = node.find(".//table/tr/td/span[@class='nobr']/h2[@class='r']")
            if calculator is not None:
                e.title = 'Calculator'
                e.description = ''.join(calculator.itertext())
                return e

            parent = node.getparent()

            words = parent.find(".//ol/div[@class='g']/div/table/tr/td/h3[@class='r']")
            if words is not None:
                e.title = 'Google Translate'
                e.add_field(name='Input', value=words[0].text, inline=True)
                e.add_field(name='Out', value=words[1].text, inline=True)
                return e

            weather = parent.find(".//ol//div[@class='e']")
            if weather is None:
                return None

    @client.command(name='Google Search',
                    description='Searches Google',
                    pass_context=True)

    async def gsearch(ctx, *, query):
        if not embed_perms(ctx.message):
            config = load_optional_config()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(query) + "&start=" + '1' + "&key=AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4" + "&cx=008921493878794350931:tioeliy7j1y") as resp:
                result = json.loads(await resp.txt())
            return await ctx.send(result['items'][['link']]['snippet'])
    try:
        entries, root = await get_google_entries(query)
        card_node = root.find(".//div[@id='topstuff']")
        card = self.parse_google_card(card_node)

        # return return the snippet section of the links + websites

client = Bot(command_prefix=BOT_PREFIX)
client.run(TOKEN)



