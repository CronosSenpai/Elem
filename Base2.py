import discord 
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

TOKEN= 'NjkxMjYyNDYyMDQwOTk3ODk4.XndaXg.g8y1R8EZZPlVEj9SCbQ6ytlYavg' 
BOT_PREFIX = '.'


bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print('ok')


@bot.command(pass_context=True, aliases=['j', 'joi'])
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
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
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
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Dowloading audio now\n')
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".webm"):
            name = file
            print(f"Renamed file : {file}\n")
            os.rename(file, "song.mp3")


    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07


    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname}")
    print("playing\n")

bot.run(TOKEN)