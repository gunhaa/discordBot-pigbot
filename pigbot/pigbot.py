import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp as youtube_dl
import asyncio
import rag


# 환경 변수를 .env 파일에서 로딩
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True
 
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=intents,
    help_command=None  # 기본 도움말 명령어 제거
)

# intents = discord.Intents.all()
# bot = commands.Bot(command_prefix='!', intents=intents, help_command = None)

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''
 
 
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
 
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}
 
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
 
 
# youtube 음악과 로컬 음악의 재생을 구별하기 위한 클래스 작성.
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
 
        self.data = data
 
        self.title = data.get('title')
        self.url = data.get('url')
 
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
 
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
 
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
 
 
# 음악 재생 클래스. 커맨드 포함.
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""
        
        channel = ctx.author.voice.channel
 
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
 
        await channel.connect()
 
   
    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""
        if ctx.voice_client is None:
            await ctx.send("봇이 음성 채널에 연결되지 않았습니다.")
            return

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            if player:
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                await ctx.send(f'Now playing: {player.title}')
            else:
                await ctx.send("음악을 재생하는 데 실패했습니다.")
 
    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
 
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
 
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")
 
    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
 
        await ctx.voice_client.disconnect()
        
    @commands.command()
    async def pause(self, ctx):
        ''' 음악을 일시정지 할 수 있습니다. '''
 
        if ctx.voice_client.is_paused() or not ctx.voice_client.is_playing():
            await ctx.send("음악이 이미 일시 정지 중이거나 재생 중이지 않습니다.")
            
        ctx.voice_client.pause()
            
    @commands.command()
    async def resume(self, ctx):
        ''' 일시정지된 음악을 다시 재생할 수 있습니다. '''
 
        if ctx.voice_client.is_playing() or not ctx.voice_client.is_paused():
            await ctx.send("음악이 이미 재생 중이거나 재생할 음악이 존재하지 않습니다.")
            
        ctx.voice_client.resume()
 
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
 
 

 
 
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
 
 
async def main():
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start(DISCORD_TOKEN)
 


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
    **!join** 음성채팅 입장
    **!play {link}** 유튜브 음악 재생
    **!volume {num}** 볼륨 조절
    **!stop** 음악 정지
    **!pause** 음악 일시 중지                          
    **!resume** 음악 재개                          
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

asyncio.run(main())

