import discord

def init(bot):
    @bot.event
    async def on_ready():
        # Bot状态：オンゲキをプレイ中
        await bot.change_presence(activity=discord.Game(name='オンゲキ'))
        print(f'Bot logged in as {bot.user}')