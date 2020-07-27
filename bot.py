import discord
import json
import lib.gradient
import os
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
    if message.author == client.user:
        return

    if message.content == '!gradient':
        print(f'Generating gradient for {message.author}')

        lib.gradient.createRandomGradient(filename=message.author.id)
        print(f'Gradient {message.author.id}.png generated, sending')

        gradientFile = discord.File(f'{message.id}.png', filename='gradient.png')
        await message.channel.send(file = gradientFile, content = f'{message.author.mention} here you go!')
        os.remove(f'{message.author.id}.png')

client.run(DISCORD_TOKEN)