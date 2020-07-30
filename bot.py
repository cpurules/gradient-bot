import discord
import json
import lib.gradient
import os
import random
import sys

from discord.ext import commands

def loadWordLists():
    global adjectives, nouns
    adjectives = open('english-adjectives.txt').read().splitlines()
    nouns = open('english-nouns.txt').read().splitlines()

# get preference
if not os.path.exists('preferences.json'):
    print('preferences.json missing!  Exiting...')
    sys.exit()

with open('preferences.json') as f:
    prefs = json.load(f)

if not 'DISCORD_TOKEN' in prefs:
    print('DISCORD_TOKEN missing from preferences.json!  Exiting...')
    sys.exit()

DISCORD_TOKEN = prefs['DISCORD_TOKEN']

bot = commands.Bot(command_prefix='!')

requesters = []

adjectives = []
nouns = []
loadWordLists()

@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected!')

@bot.command(name='gradient', help='Generate a random gradient and name it')
async def gradient(ctx, overlay=None):
    requester = ctx.author
    msg = ctx.message

    if(requester.id in requesters):
        print(f'{requester} already has a request in')
        return
    
    print(f'Generating gradient for {requester}')
    requesters.append(requester.id)

    lib.gradient.createRandomGradient(filename=msg.id, overlay=overlay, size=512)
    print(f'Gradient {msg.id}.png generated, sending')

    gradientName = random.choice(adjectives).capitalize() + ' ' + random.choice(nouns).capitalize()

    gradientFile = discord.File(f'{msg.id}.png', filename='gradient.png')

    try:
        await ctx.send(file = gradientFile, content = (f'{requester.mention} here you go!  I call this one **' + gradientName + '**'))
    except:
        print(f'Error sending gradient for {requester}')
    finally:
        os.remove(f'{msg.id}.png')
        requesters.remove(requester.id)

@bot.command(name='g', help='Shortcut for !gradient')
async def g(ctx, overlay=None):
    await gradient.invoke(ctx)

@bot.command(name='reload', help='Reload word lists for names')
async def reload(ctx):
    print(f'Reloading word list!')
    loadWordLists()

bot.run(DISCORD_TOKEN)