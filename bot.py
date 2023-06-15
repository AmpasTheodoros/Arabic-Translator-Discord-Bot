from discord.ext import commands
import discord
from deep_translator import GoogleTranslator
from langdetect import detect
import re

intents = discord.Intents.default()
intents.message_content = True

ROLE_NAME = 'Mentor'  
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    mentor_role = discord.utils.get(message.guild.roles, name=ROLE_NAME)

    # check if the role is mentioned anywhere in the message
    if mentor_role in message.role_mentions:
        content = message.content
        try:
            # detect the language of the message
            lang = detect(content)
            # if the language is not English, translate it
            if lang != 'en':
                translated_text = GoogleTranslator(source='auto', target='english').translate(content)
                await message.channel.send(f'Translated: {translated_text}')
        except Exception as e:
            print(e)

    # check if the message starts with /translate
    if message.content.startswith('/translate'):
        link = message.content.split(' ')[1]  # extract the link from the message
        match = re.search(r"https://discord.com/channels/(?P<guild_id>\d+)/(?P<channel_id>\d+)/(?P<message_id>\d+)", link)
        if match:
            channel_id = int(match.group('channel_id'))  # extract the channel ID from the link
            message_id = int(match.group('message_id'))  # extract the message ID from the link
            target_channel = bot.get_channel(channel_id)  # get the channel object
            target_message = await target_channel.fetch_message(message_id)  # get the message object
            content = target_message.content
            try:
                # detect the language of the message
                lang = detect(content)
                # if the language is not English, translate it
                if lang != 'en':
                    translated_text = GoogleTranslator(source='auto', target='english').translate(content)
                    await message.channel.send(f'Translated: {translated_text}')
            except Exception as e:
                print(e)

    await bot.process_commands(message)


bot.run('your_bot_token')  # Replace with your actual bot token
