# Shuyi Music Bot

from discord.ext import commands
import youtube_dl

TOKEN = 'NTQ1OTg0ODY4OTM3NjI5NzAw.D2f2UA.AFTB7ougi3e3U0vytq7wUZ8RPIw'

BOT_PREFIX = '.'

client = commands.Bot(command_prefix=BOT_PREFIX)

players = {}


@client.command(name='join',
                description="Joins current voice channel.",
                brief="Joins voice channel.",
                pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    server = ctx.message.server
    vc = client.voice_client_in(server)
    if client.is_voice_connected(server):
        await vc.move_to(channel)
        await client.say("I joined the voice channel: {}".format(channel))
    else:
        await client.join_voice_channel(channel)
        await client.say("I joined the voice channel: {}".format(channel))


@client.command(name='leave',
                description="Leaves voice channel.",
                brief="Leaves voice channel.",
                pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    vc = client.voice_client_in(server)
    await vc.disconnect()


@client.command(name='play',
                description='Plays music.',
                brief='Plays music. .play <URL>.',
                pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


@client.command(name='pause',
                description='Pauses music.',
                brief='Pause',
                pass_context=True)
async def pause(ctx):
    pid = ctx.message.server.id
    players[pid].pause()


@client.command(name='resume',
                description='Resumes music.',
                brief='Resumes',
                pass_context=True)
async def resumes(ctx):
        rid = ctx.message.server.id
        players[rid].resume()


@client.command(name='stop',
                description='Stops music.',
                brief='Stops',
                pass_context=True)
async def stop(ctx):
            id = ctx.message.server.id
            players[id].stop()


@leave.error
async def channel_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        await client.send_message(ctx.message.channel, 'Not in channel!')
    else:
        raise error

client.run(TOKEN)
