import discord
import util
import os
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!rate ping'):
		await message.channel.send('pong')

	
	if message.content.startswith('!rate gear image'):
		url = message.attachments[0].url
		await message.channel.send(util.call_gear_score(url))

token = os.getenv('TOKEN')
client.run(token)