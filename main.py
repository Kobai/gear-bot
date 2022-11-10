import discord
import util

client = discord.Client()


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!rate gear'):
		url = message.attachments[0].url
		await message.channel.send(util.call_gear_score(url))

with open('secrets/token.txt', 'r') as f:
	token = f.read()
client.run(token)