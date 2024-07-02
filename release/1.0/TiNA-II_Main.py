import discord
from discord.ext import commands
import asyncio

token = 'MTI1NTY3NjY5NTYwNDg4NzY1NA.G2ZLZQ.Rej98w-ojfCz0QvHQ2wFbnX8xW8IRmq3q9KKTc'

# 创建一个Bot对象，设置命令前缀为"!"，并指定intents
intents = discord.Intents.default()
intents.message_content = True # 允许Bot读取消息
bot = commands.Bot(command_prefix='!', intents=intents)

# 导入RSS源抓取转发和指令识别模块
import rss_feed
import command_recognition
import bot_activity

# 初始化这两个模块
rss_feed.init(bot)
command_recognition.init(bot)
bot_activity.init(bot)

# 自动刷新RSS源并转发RSS消息
@bot.event
async def rss_loop():
    print(f'Bot logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name='オンゲキ'))
    while True:
        await rss_feed.refresh_and_forward()
        await asyncio.sleep(60)  # 每60秒检查一次更新

@bot.event
async def on_ready():
    global rss_task
    # 创建一个新的Task对象来运行rss_loop函数
    rss_task = asyncio.create_task(rss_loop())

bot.run(token)