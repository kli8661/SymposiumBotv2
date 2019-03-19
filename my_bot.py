# Main runner for the bot.
import testing
from discord.ext.commands import Bot

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D2f2UA.AFTB7ougi3e3U0vytq7wUZ8RPIw'
BOT_PREFIX = '.'
client = Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

testing.on_ready()
testing.ping()
testing.eight_ball()
testing.clear()
testing.square()
testing.bitcoin()
testing.help_me()
testing.list_servers()
testing.join()
testing.leave()
testing.hot_posts()
testing.rsearch()
testing.timeout_error()
testing.on_command_error()
testing.value_error()
testing.missing_argument_error()
# sub_exists()


client.run(TOKEN)
