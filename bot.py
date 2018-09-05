import discord
import asyncio
import boto3
import json

from boto3.dynamodb.conditions import Key

client = discord.Client()

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
messages = dynamodb.Table('messages')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    print(message.author)
    print(message.content)
    if message.content.startswith('!help') or \
       message.content.lower().startswith('fatalis help'):
        await client.send_message(message.channel,
                                  'Hello CMDR' + str(message.author) + '\n' +
                                  'You can ask me the following\n' +
                                  '!sleep- I will sleep for 5 seconds\n' +
                                  '!mission or fatalis mission \
                                   - Get the latest mission info\n' +
                                  '!fetchbeer - saves going to the fridge'
                                  )

    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.lower().startswith('fatalis mission') or \
         message.content.lower().startswith('!mission'):
        await client.send_message(message.channel, 'Mission')
        info = messages.query(
            KeyConditionExpression=Key('title').eq('mission')
            )
        return_message = info['Items'][0]['information']
        await client.send_message(message.author, return_message)

    elif message.content.startswith('!fetchbeer'):
        await client.send_message(message.channel, ':beer:')

    elif 'cheers' in message.content.lower():
        await client.send_message(message.channel, ':beers:')


client.run('<token>')
