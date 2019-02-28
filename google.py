import pprint
import sys
from discord.ext.commands import Bot
from apiclient.discovery import build

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

BOT_PREFIX = '$'
api_key = 'AIzaSyATGAnmCuJHlvsdVn21472sJPuAiEanSY4'
service = build('Discord', 'v1', developerKey=api_key)

request = service.volumes().list(source='public', q='Test')

response = request.execute()
pprint.pprint(response)


client = Bot(command_prefix=BOT_PREFIX)


client.run(TOKEN)
