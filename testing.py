# Here are some general/testing methods that were worked on by all of us.

import config
import praw
import random
import asyncio
import aiohttp
import json
import discord
import urllib.parse
from bs4 import BeautifulSoup
from lxml import etree
from discord import Game
from discord.ext import commands
from discord.ext.commands import Bot
from utils.checks import load_optional_config, embed_perms
from prawcore import NotFound

TOKEN = config.discord_token
BOT_PREFIX = '.'
players = {}
m_api_key = config.mapikey
m_cx_key = config.mcxkey
client = Bot(command_prefix=BOT_PREFIX)
reddit = praw.Reddit(client_id=config.rclientid,
                     client_secret=config.rclientsecret,
                     user_agent=config.ruseragent)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name=" .help"))
    print("Logged in as " + client.user.name)


@client.command(name='ping',
                description="Tests if the bot is alive.",
                brief="Ping and Pong.")
async def ping():
    await client.say("pong")


@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond. \n[.8ball <question>]",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
        'Impossible',
        'Try asking a better question',
        'Certainly',
        'Of Course'
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command(name='clear',
                description='Clears the amount of lines in the text channel the user wants.',
                brief='Clears a certain amount of messages. \n[.clear <amount>]',
                pass_context=True)
async def clear(context, amount):
    amount = amount
    channel = context.message.channel
    lines = []
    async for message in client.logs_from(channel, limit=int(amount) + 1):
        lines.append(message)
    await client.delete_messages(lines)
    await client.say('Cleared ' + amount + ' messages!')


@client.command(name='square',
                description="Squares a number.",
                brief="Squares a number. \n[.square <number>]")
async def square(number):
    try:
        squared_value = float(number) * float(number)
        await client.say(str(number) + " squared is " + str(squared_value))
    except ValueError:
        await client.say('Not a number, use .square <number>.')


@client.command(name='bitcoin',
                description="Check's Bitcoin Price to USD",
                brief="Bitcoin Price.")
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


@client.command(name='join',
                description="Joins current voice channel.",
                brief='Joins voice channel.',
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
                brief='Plays Music.\n'
                      '[.play <URL>]',
                pass_context=True)
async def play(ctx, url):
    try:
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()
        await client.say('Playing')
    except AttributeError:
        await client.say('Not in channel.')


@client.command(name='pause',
                description='Pauses music.',
                brief='Pause Music',
                pass_context=True)
async def pause(ctx):
    try:
        pid = ctx.message.server.id
        players[pid].pause()
        await client.say('Paused')
    except KeyError:
        await client.say('Not in channel / Not playing music.')


@client.command(name='resume',
                description='Resumes music.',
                brief='Resumes Music',
                pass_context=True)
async def resume(ctx):
    try:
        rid = ctx.message.server.id
        players[rid].resume()
        await client.say('Resumed')
    except KeyError:
        await client.say('Not in channel / Not playing music.')


@client.command(name='stop',
                description='Stops music.',
                brief='Stops Music',
                pass_context=True)
async def stop(ctx):
    rid = ctx.message.server.id
    players[rid].stop()
    await client.say('Music Stopped')


@client.command(name='hot_posts',
                description='Grabs the hot posts from a subreddit of the users choice.',
                brief='Grabs hot posts from subreddit. \n[.hot_posts <subreddit> <number of posts>]',
                pass_context=True)
@commands.cooldown(1.0, 10.0, commands.BucketType.user)
async def hot_posts(ctx, subreddit, amount):
    channel = ctx.message.channel
    if sub_exists(subreddit):
        subreddit = subreddit
    else:
        await client.send_message(channel, "This subreddit doesn't exist!")
    limit = int(amount)
    post_sub = reddit.subreddit(subreddit)
    hot = post_sub.hot(limit=limit + 2)
    embed = discord.Embed(
        author=subreddit,
        title='Top Posts',
        colour=discord.Colour.blue()
    )

    for submission in hot:
        if not submission.stickied:
            ratio = submission.upvote_ratio
            upvote = round((ratio * submission.score)/(2 * ratio - 1)) if ratio != 0.5 else round(submission.score/2)
            downvote = upvote - submission.score
            embed.add_field(name=str(submission.title), value='URL: ' + str(submission.url) + '\n' + 'Upvotes: ' +
                            str(submission.ups) + ', ' + 'Downvotes: ' + str(downvote), inline=False)

    await client.send_message(channel, embed=embed)


def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, include_nsfw=True, exact=True)
    except NotFound:
        exists = False
    return exists


@client.command(name='rsearch',
                description='Searches reddit.',
                brief='Searches reddit. \n[.rsearch <example search>]',
                pass_context=True)
@commands.cooldown(1.0, 10.0, commands.BucketType.user)
async def rsearch(ctx, *, query):
    channel = ctx.message.channel
    querystr = str(query)
    print(querystr)
    sub = reddit.subreddit('all')
    embed = discord.Embed(
        author=querystr,
        title='Search Results For: ' + querystr,
        colour=discord.Colour.blue()
    )
    for i in sub.search(querystr, limit=5):
        embed.add_field(name=str(i.title), value='URL: ' + str(i.url), inline=False)

    await client.send_message(channel, embed=embed)


@client.command(name='r_meme',
                description='Grabs memes.',
                brief='Grabs memes from meme subreddits.',
                pass_context=True)
@commands.cooldown(1.0, 3.0, commands.BucketType.user)
async def r_meme(ctx):
    channel = ctx.message.channel
    import random
    subredditlist = ['dankmemes', 'memes', 'deepfriedmemes', 'nukedmemes',
                     'surrealmemes', 'wholesomememes', 'comedycemetery', 'me_irl', 'bonehurtingjuice']
    sub = random.choice(subredditlist)
    print(sub)
    post_sub = reddit.subreddit(sub)
    posts = [post for post in post_sub.new(limit=100)]
    random_post_number = random.randint(0, 100)
    random_post = posts[random_post_number]
    url = random_post.url
    print(url)
    if url.endswith('.jpg') | url.endswith('.jpeg') | url.endswith('.png') | url.endswith('gif'):
        if not random_post.stickied:
            await client.send_message(channel, sub + '\n' + url)
    else:
        await r_meme()
        await client.send_message('Unable to find meme, please try again.')


def write_config_value(section, key, value):
    with open("settings/" + section + ".json", "r+") as fp:
        opt = json.load(fp)
        opt[key] = value
        fp.seek(0)
        fp.truncate()
        json.dump(opt, fp, indent=4)


def get_config_value(section, key, fallback=""):
    with open("settings/" + section + ".json", "r") as f:
        try:
            value = json.load(f)[key]
        except KeyError:
            # Value does not exist
            value = fallback
            write_config_value(section, key, fallback)
        return value


def parse_google_card(node):
    if node is None or type(node) is int:
        return None

    e = discord.Embed(colour=0x0057e7)

    calculator = node.find(".//table/tr/td/span[@class='nobr']/h2[@class='r']")
    if calculator is not None:
        e.title = 'Calculator'
        e.description = ''.join(calculator.itertext())
        return e

    parent = node.getparent()

    unit = parent.find(".//ol//div[@class='_Tsb']")
    if unit is not None:
        e.title = 'Unit Conversion'
        e.description = ''.join(''.join(n.itertext()) for n in unit)
        return e

    currency = parent.find(".//ol/table[@class='std _tLi']/tr/td/h2")
    if currency is not None:
        e.title = 'Currency Conversion'
        e.description = ''.join(currency.itertext())
        return e

    release = parent.find(".//div[@id='_vBb']")
    if release is not None:
        try:
            e.description = ''.join(release[0].itertext()).strip()
            e.title = ''.join(release[1].itertext()).strip()
            return e
        except:
            return None

    words = parent.find(".//ol/div[@class='g']/div/h3[@class='r']/div")
    if words is not None:
        try:
            definition_info = words.getparent().getparent()[1]
        except:
            pass
    else:
        try:
            e.title = words[0].text
            e.description = words[1].text
        except:
            return None
    for row in definition_info:
        if len(row.attrib) != 0:
            break
        try:
            data = row[0]
            lexical_category = data[0].text
            body = []
            for index, definition in enumerate(data[1], 1):
                body.append('%s. %s' % (index, definition.text))
            e.add_field(name=lexical_category, value='\n'.join(body), inline=False)
        except:
            continue
        return e

    words = parent.find(".//ol/div[@class='g']/div/table/tr/td/h3[@class='r']")
    if words is not None:
        e.title = 'Google Translate'
        e.add_field(name='Input', value=words[0].text, inline=True)
        e.add_field(name='Out', value=words[1].text, inline=True)
        return e

    time_in = parent.find(".//ol//div[@class='_Tsb _HOb _Qeb']")
    if time_in is not None:
        try:
            time_place = ''.join(time_in.find("span[@class='_HOb _Qeb']").itertext()).strip()
            the_time = ''.join(time_in.find("div[@class='_rkc _Peb']").itertext()).strip()
            the_date = ''.join(time_in.find("div[@class='_HOb _Qeb']").itertext()).strip()
        except:
            return None
        else:
            e.title = time_place
            e.description = '%s\n%s' % (the_time, the_date)
            return e

    weather = parent.find(".//ol//div[@class='e']")
    if weather is None:
        return None

    location = weather.find('h3')
    if location is None:
        return None

    e.title = ''.join(location.itertext())

    table = weather.find('table')
    if table is None:
        return None

    try:
        tr = table[0]
        img = tr[0].find('img')
        category = img.get('alt')
        image = 'https:' + img.get('src')
        temperature = tr[1].xpath("./span[@class='wob_t']//text()")[0]
    except:
        return None
    else:
        e.set_thumbnail(url=image)
        e.description = '*%s*' % category
        e.add_field(name='Temperature', value=temperature)

    try:
        wind = ''.join(table[3].itertext()).replace('Wind: ', '')
    except:
        return None
    else:
        e.add_field(name='Wind', value=wind)

    try:
        humidity = ''.join(table[4][0].itertext()).replace('Humidity: ', '')
    except:
        return None
    else:
        e.add_field(name='Humidity', value=humidity)

    return e


@client.command(name='g',
                description='Searches google.',
                brief='Searches google. \n[.g <example search>]',
                pass_context=True)
async def g(ctx, *, query):
    """Google web search. Ex: >g what is discordapp?"""
    channel = ctx.message.channel
    print(query)
    try:
        entries, root = await get_google_entries(query)
        card_node = root.find(".//div[@id='topstuff']")
        card = parse_google_card(card_node)
    except RuntimeError as e:
        await client.send_message(channel, str(e))
    else:
        if card:
            value = '\n'.join(entries[:2])
            if value:
                card.add_field(name='Search Results', value=value, inline=False)
            return await client.send_message(channel, embed=card)
        if len(entries) == 0:
            return await client.send_message(channel, 'No results.')
        next_two = entries[1:3]
        if next_two:
            formatted = '\n'.join(map(lambda x: '<%s>' % x, next_two))
            msg = '{}\n\n**See also:**\n{}'.format(entries[0], formatted)
        else:
            msg = entries[0]
        await client.send_message(channel, msg)


@client.command(name='i',
                description='Searches google images.',
                brief='Searches google images. \n[.i <example search>]',
                pass_context=True,
                aliases=['image', 'img'])
async def i(ctx, *, query):
    """Google image search. >i Lillie pokemon sun and moon"""
    channel = ctx.message.channel
    config = load_optional_config()
    if query[0].isdigit():
        item = int(query[0])
        query = query[1:]
    else:
        item = 0
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(
                query) + "&start=" + '1' + "&key=" + config.mapikey + "&cx=" + config.mcxkey + "&searchType=image") as resp:
            if resp.status != 200:
                if not config.mapikey or not config.mcxkey:
                    return await client.send_message(channel,
                        '.' + "You don't seem to have image searching configured properly. Refer to the wiki for details.")
                return await client.send_message(channel, '.' + 'Google failed to respond.')
            else:
                result = json.loads(await resp.text())
                try:
                    result['items']
                except:
                    return await client.send_message(channel,
                        '.' + 'There were no results to your search. Use more common search query or make sure you have image search enabled for your custom search engine.')
                if len(result['items']) < 1:
                    return await client.send_message(channel,
                        '.' + 'There were no results to your search. Use more common search query or make sure you have image search enabled for your custom search engine.')
                em = discord.Embed()
                em.set_image(url=result['items'][item]['link'])
                show_search = get_config_value("optional_config", "show_search_term")
                if show_search == "True":
                    em.set_footer(text="Search term: \"" + query + "\"")
                await client.send_message(channel, content=None, embed=em)


async def get_google_entries(query):
    params = {
        'q': query,
        'safe': 'off'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows ; Win64; x64)'
    }
    entries = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.google.com/search', params=params, headers=headers) as resp:
            if resp.status != 200:
                config = load_optional_config()
                async with session.get("https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(query) + "&start=" + '1' + "&key=" + config.mapikey + "&cx=" + config.mcxkey) as resp:
                    result = json.loads(await resp.text())
                return None, result['items'][0]['link']

            try:
                root = etree.fromstring(await resp.text(), etree.HTMLParser())
                search_nodes = root.findall(".//div[@class='g']")
                for node in search_nodes:
                    url_node = node.find('.//h3/a')
                    if url_node is None:
                        continue
                    url = url_node.attrib['href']
                    if not url.startswith('/url?'):
                        continue
                    url = urllib.parse.parse_qs(url[5:])['q'][0]
                    entries.append(url)
            except NameError:
                root = BeautifulSoup(await resp.text(), 'html.parser')
                for result in root.find_all("div", class_='g'):
                    url_node = result.find('h3')
                    if url_node:
                        for link in url_node.find_all('a', href=True):
                            url = link['href']
                            if not url.startswith('/url?'):
                                continue
                            url = urllib.parse.parse_qs(url[5:])['q'][0]
                            entries.append(url)
    return entries, root


@client.command(name='testg',
                pass_context=True)
async def testg(ctx, *, query):
    channel = ctx.message.channel
    querystr = str(query)
    url = "https://www.googleapis.com/customsearch/v1?q=" + urllib.parse.quote_plus(query) + "&start=" + '1' + "&key=" + config.mapikey + "&cx=" + config.mcxkey
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    embed = discord.Embed(
        author=querystr,
        title='Search Results For: ' + querystr,
        colour=discord.Colour.blue()
    )
    embed.add_field(name=str(str(data["title"])), value='URL: ' + str(data["link"]), inline=False)
    await client.send_message(channel, embed)


@rsearch.error
@hot_posts.error
async def timeout_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You can use this every 10 seconds, please try again in {:.2f}s'.format(error.retry_after)
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@r_meme.error
async def meme_antispam(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'You can use this every 3 seconds, please try again in {:.2f}s'.format(error.retry_after)
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@play.error
@square.error
@hot_posts.error
@rsearch.error
async def missing_argument_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        msg = 'Missing required argument, use .help for more info.'
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        await client.send_message(ctx.message.channel, 'Cannot find this command!')
    else:
        raise error


@clear.error
async def value_error_clear(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        msg = 'clear: Use a number 1-99 / Not allowed to clear chat.'
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@hot_posts.error
async def value_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        msg = 'hot_posts: Use a number from 1-25.'
        await client.send_message(ctx.message.channel, msg)
    else:
        raise error


@leave.error
async def channel_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        await client.send_message(ctx.message.channel, 'Not in channel!')
    else:
        raise error


@join.error
async def isvoice_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        await client.send_message(ctx.message.channel, 'Must be in a voice channel to use .join!')
    else:
        raise error


@play.error
async def url_error(error, ctx):
    if isinstance(error, commands.CommandInvokeError):
        await client.send_message(ctx.message.channel, 'Youtube links only.')
    else:
        raise error


client.loop.create_task(list_servers())
client.run(TOKEN)
