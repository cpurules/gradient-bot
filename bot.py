import discord
import json
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

client = Discord.client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(DISCORD_TOKEN)