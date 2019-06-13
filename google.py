import config
import json
import aiohttp
from discord.ext import commands
from utils.checks import load_optional_config, embed_perms
import urllib.parse
from urllib.request import urlopen
from lxml import html
import requests
from bs4 import BeautifulSoup
from lxml import etree

BOT_PREFIX = '.'

m_api_key = config.mapikey
m_cx_key = config.mcxkey


# def google_search(search_term, api_key, cx_id, **kwargs):
# service = build("customSearch", "v1", developerKey=api_key)
# res = service.cse().list(q=search_term, cx=cx_id, **kwargs).execute()
#  return res['items']

# results = google_search('facebook', api_key, cx_key, num=2)

# for result in results
# pprint.pprint(result

#    title = result['title']
#    link = result['formattedUrl']
#    dis = result['snippet']
#    print(title)
#    print(link)
#    print(dis)

class Google:
    def parse_google__card(self, node):
        if node is None or type(node) is int:
            return None

    # https://stackoverflow.com/questions/23248017/cannot-find-reference-xxx-in-init-py-python-pycharm
        @commands.command(pass_context=True)
        async def g(self, ctx, *, query):
            if not embed_perms(ctx.message):
                config = load_optional_config()
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.googleapis.com/customsearch/v1?q=" +
                                           urllib.parse.quote_plus(query) + "&start=" +
                                           '1' + "&key=AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4" +
                                           "&cx= " + m_cx_key + config
                                           ['custom_search_engine']) as resp:
                        result = json.loads(await resp.text())
                return await ctx.send(result['items'][['link']]['snippet'])

            try:
                entries, root = await get_google_entries(query)
                card_node = root.find(".//div[@id='topstuff']")
                card = self.parse_google_card(card_node)
            except RuntimeError as e:
                await ctx.send(str(e))
            else:
                if card:
                    value = '\n'.join(entries[:2])
                    if value:
                        card.add_field(name='Search Results', value=value, inline=False)
                    return await ctx.send(embed=card)
                if len(entries) == 0:
                    return await ctx.send('No results.')
                next_two = entries[1:3]
                if next_two:
                    formatted = '\n'.join(map(lambda x: '<%s>' % x, next_two))
                    msg = '{}\n\n**See also:**\n{}'.format(entries[0], formatted)
                else:
                    msg = entries[0]
                await ctx.send(msg)


'''async def get_google_entries(query):
    params = {
        'q': query,
        'safe': 'off'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows 10; Win64; x64)'
    }
    entries = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.google.com/search', params=params, headers=headers) as resp:
            if resp.status != 200:
                config = load_optional_config()
                async with session.get("https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(
                        query) + "&start=" + '1' + "&key=" + config['google_api_key'] + "&cx=" + config[
                                           'custom_search_engine']) as resp:
                    result = json.loads(await resp.text())
                return None, result['items'][0]['link']

            try:
                root = etree.fromstring(await resp.text(), etree.HTMLParser())
                search_nodes = root.findall(".//div[@class='g']")
                for node in search_nodes:
                    url_node = node.find('.//h3/a')
                    if url_node is None:
                        continue
                    url = url_node.attrib['href']
                    if not url.startswith('/url?'):
                        continue
                    url = urllib.parse.parse_qs(url[5:])['q'][0]
                    entries.append(url)
            except NameError:
                root = BeautifulSoup(await resp.text(), 'html.parser')
                for result in root.find_all("div", class_='g'):
                    url_node = result.find('h3')
                    if url_node:
                        for link in url_node.find_all('a', href=True):
                            url = link['href']
                            if not url.startswith('/url?'):
                                continue
                            url = urllib.parse.parse_qs(url[5:])['q'][0]
                            entries.append(url)
    return entries, root
'''

async def get_google_entries(query):
   # response = json.loads(requests.get("https://www.googleapis.com/customsearch/v1?q=computerscience&start=1&key=AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4&cx=008921493878794350931:tioeliy7j1y").text)
   # url = urllib.request.urlopen("https://www.googleapis.com/customsearch/v1?q=computerscience&start=1&key=AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4&cx=008921493878794350931:tioeliy7j1y")
   # content = url.read()
   #soup = BeautifulSoup(content, 'html.parser')
#  newDictionary = json.loads(str(soup))


    url = "https://www.googleapis.com/customsearch/v1?q=computerscience&start=1&key=AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4&cx=008921493878794350931:tioeliy7j1y"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    print(data["snippet"])

