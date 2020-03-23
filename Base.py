import discord
import random
import youtube_dl
from discord.ext import commands
from discord.utils import get
import os

import config

#Prefijo de llamada
client = commands.Bot(command_prefix= '.')

players = {}

#Status 
@client.event
async def on_ready():
    print("Bot is OK.")


@client.event
async def on_member_join(member):
    print(f'{member} entro akka we')

@client.event
async def on_member_remove(member):
    print(f'{member} se fue we')

@client.command()
async def comunismo(ctx): #ctx hace que lo adicional sea ignorado
    await ctx.send(f'Fuera de aqui maldito comunista, aqui solo existen cerdos capitalistas {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['0','3','2','54', 'tetet', 'trpiac']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}') #\n pone lo siguiente en la proxima linea

@client.command(pass_context=True)
async def join(ctx): #entra en el server
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True) #sale del server
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client(guild)
    await voice_client.disconnect()


@client.command(pass_context=True)
async def play(ctx, url):
    guild = ctx.message.guild
    voice_client = guild.voice_client(guild)
    player = await voice_client.create_ytdl_player(url)
    players[guild.id] = player
    player.start()



TOKEN= config.DISCORD_TOKEN
#token
client.run(TOKEN)
