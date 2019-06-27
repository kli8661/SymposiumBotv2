# Main runner for the bot.
import config
import testing
from discord.ext.commands import Bot

TOKEN = config.discord_token
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
testing.list_servers()
testing.join()
testing.leave()
testing.play()
testing.pause()
testing.resume()
testing.stop()
testing.hot_posts()
testing.rsearch()
testing.timeout_error()
testing.on_command_error()
testing.value_error()
testing.missing_argument_error()
testing.r_meme()
testing.meme_antispam()
testing.g()
testing.i()
testing.testg()
testing.delete()

client.run(TOKEN)
