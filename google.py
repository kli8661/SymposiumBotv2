import pprint
from googleapiclient.discovery import build
from discord.ext.commands import Bot


TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'
BOT_PREFIX = '.'

m_api_key = 'AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4'
m_cx_key = '008921493878794350931:tioeliy7j1y'


def google_search(search_term, api_key, cx_id, **kwargs):
    service = build("customSearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cx_id, **kwargs).execute()
    return res['items']


results = google_search('facebook', api_key, cx_key, num=2)

for result in results:
    pprint.pprint(result)

    title = result['title']
    link = result['formattedUrl']
    dis = result['snippet']
    print(title)
    print(link)
    print(dis)

client = Bot(command_prefix=BOT_PREFIX)


client.run(TOKEN)
