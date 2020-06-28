import discord
import json
import time
from google.cloud import texttospeech

ttsclient = texttospeech.TextToSpeechClient.from_service_account_json('C:\\Users\\ethan\\Documents\\google\\Quickstart-51a28cf1263c.json')
client = discord.Client()

data = open("database.json", "r")
database = json.loads(data.read())
data.close()

flirtydata = open("flirty.json", "r")
flirtydatabase = json.loads(flirtydata.read())
flirtydata.close()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("With Amaan's Lil' Bits")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id == 434816199784792065 or message.author.id == 446748603860516894:
        if message.content.startswith("-game"):
            game = discord.Game(message.content[5:])
            await client.change_presence(status=discord.Status.online, activity=game)
        elif message.content.lower() in flirtydatabase:
            await message.channel.send(flirtydatabase[message.content.lower()])
        elif message.content.lower() in database:
            await message.channel.send(database[message.content.lower()])
    elif message.content.lower() in database:
        await message.channel.send(database[message.content.lower()])

    # if message.content.lower() == "eray called you sexy":
    #     await message.channel.send("ayo who tf u think u are")
    #     time.sleep(2)
    #     await message.guild.get_member(447530218991910942).kick()

    if message.content.startswith("-say") and message.content.lower()[5:] in database:
        if len(client.voice_clients) > 0:
            voice_client = client.voice_clients[0]
        else:
            voice_client = await message.channel.guild.voice_channels[0].connect()
        synthesis_input = texttospeech.SynthesisInput(text=database[message.content.lower()[5:]])
        voice = texttospeech.VoiceSelectionParams(language_code="en-UK", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, name="en-IN-Wavenet-A")
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = ttsclient.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        with open("output.mp3", "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to file "output.mp3"')
        source = await discord.FFmpegOpusAudio.from_probe("output.mp3", executable="ffmpeg.exe", method="fallback")
        voice_client.play(source)
        await message.add_reaction("👍")

    if message.content.startswith("-play"):
        if len(client.voice_clients) > 0:
            voice_client = client.voice_clients[0]
        else:
            voice_client = await message.channel.guild.voice_channels[0].connect()
        source = await discord.FFmpegOpusAudio.from_probe("song.mp3", executable="ffmpeg.exe", method="fallback")
        voice_client.play(source)


client.run("NzIxMzQ1MTUzNzE2OTc3NzE0.XuTVCw.FvlWWey4qmP1O73pu_AZ_Iytz6c")  # Shirley
