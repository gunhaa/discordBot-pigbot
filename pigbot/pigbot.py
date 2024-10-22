import os
import discord
from dotenv import load_dotenv
import asyncio
import rag.rag as rag
from models.Music import Music
from models.Bot import bot

# 환경 변수를 .env 파일에서 로딩
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
 

@bot.command(name='hello')
async def hello(ctx):

    prompt = '무길무길'

    await ctx.channel.send(prompt)

@bot.command(name='help')
async def help_command(ctx):

    print('실행됨')
    
    embed = discord.Embed(title="도움말", description='''
    **!hello** 봇에게 인사
    **!help** 커맨드 질문
    **!join** 음성채팅방에 봇 입장
    **!youtube** 링크 유튜브 영상 재생
    **!supervive** 슈퍼바이브 질문
    **!play {link}** 유튜브 음악 재생
    **!volume {num}** 볼륨 조절
    **!pause** 음악 일시 중지                          
    **!resume** 음악 재개
    **!exit** 봇 나가기                    
    ''', color=0xffc0cb)
    
    # 아바타가 존재하는 경우에만 URL을 사용
    avatar_url = ctx.message.author.avatar.url if ctx.message.author.avatar else None
    embed.set_footer(text=f"{ctx.message.author.name} | Pig Bot#3604", icon_url=avatar_url)
    
    await ctx.send(embed=embed)  # 메시지 전송



@bot.command(name='supervive')
async def supervive(ctx):
    
    result = rag.supervive()

    prompt = '공사중' 

    await ctx.channel.send(prompt)

#start the bot
 
async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start(DISCORD_TOKEN)
 
asyncio.run(main())

