
# @bot.event
# async def on_ready():
#   print(f'We have logged in as {bot.user.name}')


# @bot.command(name='hello')
# async def hello(ctx):

#     prompt = '무길무길'

#     await ctx.channel.send(prompt)

# @bot.command(name='help')
# async def help(ctx):
#     embed = discord.Embed(title = "도움말", description = '''
# **!hello** 봇에게 인사
# **!help** 커맨드 질문
# **!join** 음성채팅방에 봇 입장
# **!youtube** 링크 유튜브 영상 재생
# **!supervive** 슈퍼바이브 질문
# ''', color = 0xffc0cb)
    #print(vars(ctx))
    #embed.set_footer(text = f"{ctx.message.author.name} | Pig Bot#3604", icon_url = ctx.message.author.avatar_url)
    # await ctx.send(embed = embed)



# @bot.command(name='supervive')
# async def supervive(ctx):
#    prompt = '공사중' 
#    await ctx.channel.send(prompt)

# @bot.command(name='join')
# async def join(ctx):
#     if ctx.author.voice and ctx.author.voice.channel:
#         print("음성 채널 정보: {0.author.voice}".format(ctx))
#         print("음성 채널 이름: {0.author.voice.channel}".format(ctx))
#         await ctx.author.voice.channel.connect()
#     else:
#         await ctx.send("음성 채널이 존재하지 않습니다.")


# @bot.command(name='youtube')
# async def youtube(ctx):
#     prompt = '음악재생 ~~~'
#     await ctx.channel.send(prompt)



# start the bot
# bot.run(DISCORD_TOKEN)