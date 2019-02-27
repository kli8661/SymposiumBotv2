from discord.ext import commands

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D1SSSw.7QQpBnTcpERWKobvCn2J_zOZAAg'

BOT_PREFIX = '$'

client = commands.Bot(command_prefix=BOT_PREFIX)


@client.command(pass_context=True)
async def join(msg):
    join_channel = msg.message.server
    await client .join_voice_channel(join_channel)


@client.command(pass_context=True)
async def leave(msg):
    leave_channel = msg.message.server
    voice_client = client.voice_client_in(leave_channel)
    await voice_client.disconnect()


@client.command(name='p',
                description="plays an audio from youtube video",
                brief="plays music",
                aliases=['music', 'plays', 'audio'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'Impossible',
        'Try asking a better question'
    ]

client.run(TOKEN)
