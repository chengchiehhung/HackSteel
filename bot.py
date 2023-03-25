import os

import requests
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Dandy Support!'
    )

@client.event
async def on_message(message):
   
    if message.author == client.user:
        return
    print(message.content)


    
    if message.content.isdigit():
        if int(message.content)>=10000:
            url = "https://crime-data-by-zipcode-api.p.rapidapi.com/crime_data"

            querystring = {"zip":message.content}
            headers = {
                "X-RapidAPI-Key": "3405bcaaf5mshfc00339e0e741dcp1525c4jsn204dfa09738f",
                "X-RapidAPI-Host": "crime-data-by-zipcode-api.p.rapidapi.com"
            }
            zip = message.content
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()
            crime_grade = data["Overall"]['Overall Crime Grade']
            fact = data["Overall"]['Fact']
            risk_detail = data["Overall"]['Risk Detail']
            print('crime_grade: ', crime_grade)
            print('fact: ', fact)
            print('risk_detail: ', risk_detail)
            starter = 'The overall safe report in area **%s** is as below!' %zip
            securityGrade = 'Overall security grade: **%s**' %crime_grade
            await message.channel.send(starter)
            await message.channel.send(securityGrade)
            await message.channel.send(fact)
            await message.channel.send(risk_detail)
        else:
            await message.channel.send('Please send a valid zip code.')
    else:
        await message.channel.send('Please send a valid zip code.')



client.run(TOKEN)


