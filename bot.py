import discord
import json
import lib.gradient
import os
import random
import sys

# ready preference
if not os.path.exists('preferences.json'):
    print('preferences.json missing!  Exiting...')
    sys.exit()

with open('preferences.json') as f:
    prefs = json.load(f)

if not 'DISCORD_TOKEN' in prefs:
    print('DISCORD_TOKEN missing from preferences.json!  Exiting...')
    sys.exit()

if not 'DISCORD_GUILD' in prefs:
    print('DISCORD_GUILD missing from preferences.json!  Exiting...')
    sys.exit()

DISCORD_TOKEN = prefs['DISCORD_TOKEN']
DISCORD_GUILD = prefs['DISCORD_GUILD']

client = discord.Client()

requesters = []

adjectives = []
nounes = []

def loadWordList():
    adjectives = open('english-adjectives.txt').read().splitlines()
    nouns = open('english-nouns.txt').read().splitlines()

loadWordList()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
    guild = discord.utils.get(client.guilds, name=DISCORD_GUILD)
    if guild is None:
        print(f'{client.user} does not belong to {DISCORD_GUILD}!  Exiting...')
        await client.close()
        return

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user or message.author.id in requesters:
        if(message.author.id in requesters):
            print(f'{message.author} already has a request in')
        return

    if message.content == '!gradient' or message.content == '!g':
        print(f'Generating gradient for {message.author}')
        requesters.append(message.author.id)

        await getGradient(message.id)
        print(f'Gradient {message.id}.png generated, sending')

        gradientName = random.choice(adjectives).capitalize() + ' ' + random.choice(nouns).capitalize()

        gradientFile = discord.File(f'{message.id}.png', filename='gradient.png')

        try:
            await message.channel.send(file = gradientFile, content = (f'{message.author.mention} here you go!  I call this one **' + gradientName + '**'))
        except:
            print(f'Error sending gradient for {message.author}')
        finally:
            os.remove(f'{message.id}.png')
            requesters.remove(message.author.id)
    
    if message.content == '!reload':
        print(f'Reloading word list!')
        loadWordList()


async def getGradient(f):
    lib.gradient.createRandomGradient(filename=f)

client.run(DISCORD_TOKEN)