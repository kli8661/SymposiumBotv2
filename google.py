import pprint
import sys

from discord.ext.commands import Bot
from googleapiclient.discovery import build

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

BOT_PREFIX = '.'
api_key = 'AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4'
cx_key = '008921493878794350931:tioeliy7j1y'


def google_search(search_term, api_key, cx_id, **kwargs):
    service = build("customSearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cx_id, **kwargs).execute()
    return res['items']


results = google_search('facebook', api_key, cx_key, num=2)

for result in results:
    pprint.pprint(result)

client = Bot(command_prefix=BOT_PREFIX)


client.run(TOKEN)
