from discord.ext import commands
import discord
from deep_translator import GoogleTranslator
from langdetect import detect

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

    # check if the role is mentioned in the message
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

    await bot.process_commands(message)

bot.run('MTExODUzOTY3NTkzNDY1ODYyMQ.GAtRyi.xQZg-TB_jbBsylpy7qUZ446rMh_YDN_swbvF8c')
