import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
 
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=intents,
    help_command=None  # 기본 도움말 명령어 제거
)
