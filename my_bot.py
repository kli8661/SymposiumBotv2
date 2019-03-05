# Main runner for the bot.
import testing
from discord.ext.commands import Bot

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'
BOT_PREFIX = '.'
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

testing.on_ready()
testing.list_servers()
testing.join()
testing.leave()
testing.ping()
testing.eight_ball()
testing.square()
testing.bitcoin()
testing.help_me()
testing.clear()


client.run(TOKEN)
