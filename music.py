# Shuyi Music Bot

from discord.ext import commands

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

BOT_PREFIX = '$'

client = commands.Bot(command_prefix=BOT_PREFIX)


@client.command(name='join',
                description="Joins current voice channel.",
                brief="Joins voice channel."
                , pass_context=True)
async def join(msg):
    join_channel = msg.message.server
    await client .join_voice_channel(join_channel)


@client.command(name='leave',
                description="Leaves voice channel.",
                brief="Leaves voice channel."
                , pass_context=True)
async def leave(msg):
    leave_channel = msg.message.server
    voice_client = client.voice_client_in(leave_channel)
    await voice_client.disconnect()


client.run(TOKEN)
