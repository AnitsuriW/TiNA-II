import re

import discord

import rss_feed
import random

from discord.ext import commands

def init(bot):
    # 设置一个同步命令，将下面的命令都同步到Discord中去
    @bot.command()
    @commands.has_permissions(administrator=True) # 检查权限，只有管理员才能使用命令'!synccommands'
    async def synccommands(ctx):
        await bot.tree.sync()
        await ctx.send("同步完成")

    # 定义一个异步函数来响应'ping'命令
    @bot.hybrid_command()
    async def ping(ctx):
        """测试机器人是否在线"""
        await ctx.send("むむ、ターゲット発見！\n千夏☆みさいる、ロックオン！")  # 当用户输入'/ping'时，bot回复'千夏☆みさいる、ロックオン！'

    @bot.event
    async def on_message(message):
        if re.search(r'千夏怎么了|千夏どうしたの',message.content):
            # 发送指定图片
            file_path = '/home/moka/TiNA-II_Disocrd_Bot/picture/mita_nico_wara.jpg'
            with open(file_path, 'rb') as f:
                picture = discord.File(f)
                await message.reply(file=picture)

        if re.search(r'尘白',message.content):
            # 发送指定图片
            file_path = '/home/moka/TiNA-II_Disocrd_Bot/picture/[P1]庆典开始喽~[1080P 高清].mp4'
            with open(file_path, 'rb') as f:
                video = discord.File(f)
                await message.reply(file=video)


        # 当发送にゃんにゃん的时候，千夏会回复にゃ～ん
        if re.search(r'にゃん|にゃーん',message.content):
            await message.reply("にゃ～ん")

        # 处理命令
        await bot.process_commands(message)

    # 当用户输入‘/ongekihdd'时，bot回复教程链接
    # @bot.hybrid_command()
    # async def ongekihdd(ctx):
    #     """发送最新最热SDDT教程"""
    #     await ctx.send("https://performai.notion.site/O-N-G-E-K-I-Bright-Memory-7264d5d8b3ce4920b94b422359c6b9d8")


    # 手动刷新RSS源指令
    @bot.hybrid_command()
    async def rss_renew(ctx):
        """手动刷新RSS并进行转发"""
        await rss_feed.refresh_and_forward()  # 调用rss_feed模块的refresh_and_forward函数
        await ctx.send("千夏完成了RSS源的刷新以及发送信息的工作了哦~\n千夏頑張ったよ！ほめてほめてー")

    # 添加 /roll 指令
    @bot.hybrid_command()
    async def roll(ctx, *, choices: str = None):
        """从提供的选项中随机选择一个"""
        if not choices:
            await ctx.send("请提供一些选项，例如：/roll 1 2 3 4")
            return
        choices_list = choices.split()
        selected = random.choice(choices_list)
        await ctx.send(f"千夏觉得 {selected} 比较好哦！")