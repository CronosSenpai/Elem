import discord 
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

import config
from Music import Music

TOKEN = config.DISCORD_TOKEN
BOT_PREFIX = '.'

infoMusic = Music()

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print('ok')


@bot.command(pass_context=True, aliases=['j', 'joi'], invoke_without_subcommand=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")
    
    await ctx.send(f"Joined {channel}")



@bot.command(pass_context = True, aliases=['l' , 'lea'])
async def leave(ctx):
    voice = get(bot.voice_clients, guild= ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {voice.channel}")
        await ctx.send(f" The bot has left {voice.channel}")

    else:
        print("Bot se fue del canal")
        await ctx.send("Don't think i am in a voice channel")

@bot.command(pass_context=True, alisases=['p', 'pla'])
async def play(ctx, url: str):
    song_there = os.path.isfile("./audio/song.mp3")
    try:
        if song_there:
            os.remove("./audio/song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everython ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessores': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio/song.mp3',

    }

    ytdl = youtube_dl.YoutubeDL(ydl_opts)
    print('Dowloading audio now\n')
    ytdl.download([url])
    dataMusic = ytdl.extract_info(url=url)
    

    '''
    for file in os.listdir("./audio"):
        if file.endswith(".webm"):
            name = file
            print(f"Renamed file : {file}\n")
            os.rename(file, "./audio/song.mp3")
    '''
    infoMusic.isPlaying = True
    infoMusic.currentSong = dataMusic['title']
    voice.play(discord.FFmpegPCMAudio("./audio/song.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07


    #nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {dataMusic['title']}")
    print("playing\n")

@bot.command(pass_context = True)
async def current(ctx):
    voice = get(bot.voice_clients, guild= ctx.guild)

    if voice and voice.is_connected():
        if infoMusic.isPlaying:
            await ctx.send(f" Current playing: {infoMusic.currentSong}")
        else:
            await ctx.send("Actualmente no se esta reproduciendo nada")

    else:
        print("Bot se fue del canal")
        await ctx.send("Don't think i am in a voice channel")


bot.run(TOKEN)