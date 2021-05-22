import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import random
import time
import datetime
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.members = True
prefix = '#'
Name = 'mattbaddlesmere'
startDate = datetime.datetime(2020,10,15,18).timestamp()  #1602781200 #Unix timestamp for 15/10/2020 at 18:00:00

client = commands.Bot(command_prefix=prefix, intents=intents)

@client.event
async def on_ready():
    global guild
    global channels
    global Gavin

    try:
        for guild in client.guilds:
            if guild.name is GUILD:
                break
        channels = guild.text_channels
        for member in guild.members:
            if member.name == Name:
                Gavin = member

        print(f'{client.user.name} is connected to {guild}')
        file = open('run.txt', 'r')
        if file.read() == 'False':
            file.close()
            file = open('run.txt', 'w')
            file.write('True')
            message = 'Hello! I am £100Bot, and I am here to remind @everyone that '+Gavin.mention+' owes Matt £100 on a regular basis!'
            await client.get_channel(channels[0].id).send(message)
        file.close()

        checkTimeOfDay.start()
    except NameError:
        print('Failed to Connect')

@client.command(name='paid')
async def paid(ctx):
    message = 'Oh my God @everyone, it finally happened! Gavin paid Matt £100! My work here is done'
    await client.get_channel(channels[0].id).send(message)
    await client.get_guild(guild.id).leave()
    quit()
    #Add some final stats, such as how long it was, how much he would have had to pay with interest

@client.event
async def on_member_update(before, after):
    if (after.name == Name) and (after.status is discord.Status.online):
        print(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'), 'Gavin Online')
        roll = random.randint(1, 20)
        print('Roll:', roll)
        if roll < 5:
            await send_Message()
        print()

@tasks.loop(hours=6.0)
async def checkTimeOfDay():
    print(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'), 'Time Trigger')
    roll = random.randint(1, 20)
    print('Roll:', roll)
    if roll >= 10:
        await send_Message()
    print()

@client.event
async def on_raw_message_delete(payload):
    channel = payload.channel_id
    await asyncio.sleep(5)
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
        if str(entry.target) == '£100Bot#5599':
            if str(entry.user) != 'mattbaddlesmere#0426':
                if (datetime.datetime.utcnow()-entry.created_at).total_seconds() < 300:
                    print(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'), 'Message Deleted by',str(entry.user))
                    await send_Message(channel)
                    await send_Message(channel)
                print()

async def send_Message(channel=None):
    message = messages()
    print('Sending Message:', message)
    if channel:
        await client.get_channel(channel).send(message)
    else:
        await client.get_channel(channels[random.randint(0, len(channels) - 1)].id).send(message)

def messages():
    options = [
        str(Gavin.mention) + ' you owe Matt £100',
        'Has '+str(Gavin.mention)+' paid Matt £100? No',
        str(Gavin.mention) + ' remains in debt to Matt',
        'My only purpose is to make sure ' + str(Gavin.mention) + ' does not forget he lost a bet for £100',
        str(Gavin.mention) + ' has owed Matt £100 for about ' + str(int((time.time() - startDate)/(60*60*24)))+' days',
        'If Matt charged 1% interest daily, ' + str(Gavin.mention) + ' would owe Matt £' + str(round(100*1.01**(int((time.time() - startDate)/(60*60*24))),2)),
        str(Gavin.mention) + ', Matt now accepts payments in various cryptocurrencies',
        str(Gavin.mention) + ' could have paid £' + str(round(100/int((time.time() - startDate)/(60*60*24)),2)) + ' a day to fully pay back his debt by today!',
        str(Gavin.mention) + ' can pay Matt in crypto to his wallet: 0xF5913ED5424D902dE5F5202cbEB241F647f7F321',
        str(Gavin.mention) + ' to be completely honest, Matt does not actually care, but its a very good meme',
        'https://www.gov.uk/make-court-claim-for-money, it is only a click away ' + str(Gavin.mention) + '...',
        '(((21+5)×(10-2))÷2)-(7+(2×5))=100, which just happens to be the same amount that ' + str(Gavin.mention) + ' owes Matt',
        'Just like there are 100 years in a Century, ' + str(Gavin.mention) + ' owes Matt £100',
        'Let °C = £, if ' + str(Gavin.mention) + ' were water, he would be boiling with the amount he owes Matt',
        'Did you know that the sum of the first 9 prime numbers equals 100, the same amount that ' + str(Gavin.mention) + ' owes Matt',
        'Did you know that the sum of the first 10 odd numbers equals 100, the same amount that ' + str(Gavin.mention) + ' owes Matt',
        'If you had £100 billion , you could spend £3 million a day, every day, for the next 100 years; Matt is only asking ' + str(Gavin.mention) + ' for £100',
        'In 1950, £100 would be worth £3000 today, you are lucky we are in 2021 ' + str(Gavin.mention),
        'The average male in the UK lives to 79, so if ' + str(Gavin.mention) + ' paid Matt £' + str(round(100/(79-22),2)) + ' a year he would fully pay back £100 before he dies',
        'A good quality pigeon is worth £20-£30. Matt could have 3-5 pigeons if ' + str(Gavin.mention) + ' paid him £100'
        'Matt really hopes that ' + str(Gavin.mention) + 'will be paying him his £100 as soon as he has it, like he said he would and not on other things...'
    ]
    return options[random.randint(0,len(options)-1)]

client.run(TOKEN)