import random
import os, os.path
import asyncio

import discord

lSongQueue = []
client = discord.Client(status = "lul")
voiceClient = None
channel = None


def getAllSongs():
    return [file for file in os.listdir("songs//") if os.path.isfile(os.path.join("songs//", file))]


async def addRandomSongToQueue():
    global lSongQueue, channel, voiceClient

    sSong = random.choice(getAllSongs())
    lSongQueue.append(sSong)
    if voiceClient.is_playing():
        await channel.send("🕒 Adding to queue: " + sSong.replace("-"," ").replace(".mp3","").replace(" Sidhu"," - Sidhu"))


async def changeSongs():
    global voiceClient

    while (True):
        if len(lSongQueue) > 0 and (not voiceClient.is_playing()):
            await playSong()
        await asyncio.sleep(1)


async def playSong():
    global lSongQueue, channel, voiceClient

    await channel.send("🎵 Playing: " + lSongQueue[0].replace("-", " ").replace(".mp3", "").replace(" Sidhu"," - Sidhu"))
    voiceClient.play(discord.FFmpegPCMAudio("songs//" + lSongQueue[0]))
    lSongQueue.pop(0)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global voiceClient, lSongQueue, channel

    if message.author == client.user:
        return

    if "best" in message.content and "singer" in message.content:
        await message.channel.send('Sidhu Moosewala is the bestest singer!')

    if "stop" in message.content:
        await message.channel.send('Prove you are a Karan Aujla Hater! Write "I hate Karan Aujla"')

    if "i hate karan" in message.content.lower():
        await message.channel.send("Stopping the song!")
        voiceClient.stop()

    if ("karan" in message.content or "aujla" in message.content) and ("bekar" in message.content or "bekaar" in message.content):
        channel = message.channel

        await channel.send('Karan Aujla Bekar Hai!')

        try:
            voiceClient = await message.author.voice.channel.connect (timeout = 10.0, reconnect = False)
        except discord.errors.ClientException:
            pass

        await addRandomSongToQueue()
        if not voiceClient.is_playing():
            await playSong()


client.loop.create_task (changeSongs())
client.run ('NzA2NjEyNDgzNDIyNjgzMjU3.Xq80kg.NUmwjZB_qz0PZ5uYfRur-QXHfA8')