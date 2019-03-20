# Shuyi Music Bot

from discord.ext import commands

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D2f2UA.AFTB7ougi3e3U0vytq7wUZ8RPIw'

BOT_PREFIX = '.'

client = commands.Bot(command_prefix=BOT_PREFIX)


@client.command(name='join',
                description="Joins current voice channel.",
                brief="Joins voice channel."
                , pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(name='leave',
                description="Leaves voice channel.",
                brief="Leaves voice channel."
                , pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    vc = client.voice_client_in(server)
    await vc.disconnect()


client.run(TOKEN)
