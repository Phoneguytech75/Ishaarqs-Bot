import discord
import os
import time
import requests
import json
import random
from discord import FFmpegPCMAudio
from pypresence import Presence
import discord.ext
from googleapiclient.discovery import build
from discord_slash import SlashCommand, SlashContext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
#^ basic imports for other features of discord.py and python ^

client = discord.Client()

client = commands.Bot(command_prefix = '.') #put 
slash = SlashCommand(client, sync_commands=True)
#your own prefix here

google_api = (os.getenv("google_key"))

@client.event
async def on_ready():
    print("bot online") 
    game = discord.Game(f'{str(len(client.guilds))} servers')
    await client.change_presence(status=discord.Status.online, activity=game)
    
@client.command()
async def ping(ctx):
    await ctx.send("pong!") #simple command so that when you type "!ping" the bot will respond with "pong!"

@client.command()
async def say(ctx, *, text):
   await ctx.channel.purge(limit=1)
   await ctx.send(text)



@slash.slash(name="say", description="make the bot say something")
async def slashsay(ctx, *, text):
  await ctx.send(text)


@client.command()
async def kick(ctx, member : discord.Member):
    try:
        await member.kick(reason=None)
        await ctx.send("kicked "+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("bot does not have the kick members permission!")

@slash.slash(name="Kick", description="kicks a person out")
async def slashkick(ctx, member : discord.Member):
    try:
        await member.kick(reason=None)
        await ctx.send("kicked "+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("bot does not have the kick members permission!")


@client.command()
async def source(ctx):
  await ctx.send("https://github.com/Phoneguytech75/Ishaarqs-Bot")

@client.command()
async def commands(ctx):
  with open('commands.txt', 'r') as cmds:
    embed=discord.Embed(title="Ishaarq's Epic Commands",
    description=cmds.read(),color=0x3080ff)
    await ctx.send(embed=embed)

@slash.slash(name="Commands", description="shows commands")
async def slashcommands(ctx):
  with open('commands.txt', 'r') as cmds:
    embed=discord.Embed(title="Ishaarq's Epic Commands",
    description=cmds.read(),color=0x3080ff)
    await ctx.send(embed=embed)


@client.command()
async def scott(ctx):
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    source = FFmpegPCMAudio('scott.wav')
    play = voice.play(source)


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    print("i'm out of the voice channel")

@client.command()
async def iphone(ctx, member : discord.Member):
  image_url = member.avatar_url
  url = requests.get(f'https://nekobot.xyz/api/imagegen?type=iphonex&url={image_url}')
  json_data = json.loads(url.text)
  image_output = json_data['message']
  await ctx.send(image_output)

@client.command()
async def urban(ctx, *, word):
  img='https://wjlta.files.wordpress.com/2013/07/ud-logo.jpg'
  cap_word = word.capitalize()
  url = requests.get(f'https://api.urbandictionary.com/v0/define?term={word}')
  json_data = json.loads(url.text)
  randomint = random.randint(0, 5)
  define = json_data['list'][randomint]['definition']
  link = json_data['list'][randomint]['permalink']
  embed=discord.Embed(title=cap_word, url=link)
  embed.set_image(url=img)
  embed.add_field(name='Definition', value=define)
  await ctx.send(embed=embed)

client.run(os.getenv("TOKEN")) #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!