import feedparser
import asyncio
from lxml import html

# 定义rss_urls和prev_entry_links为全局变量
rss_urls = [
    'RSS_URL1',
    'RSS_URL2'
]
prev_entry_links = [''] * len(rss_urls)

# 定义bot为全局变量
bot = None

def init(bot_instance):
    global bot
    bot = bot_instance

# 手动刷新RSS源并转发消息
async def refresh_and_forward():
    global rss_urls, prev_entry_links, bot  # 声明rss_urls和prev_entry_links为全局变量
    for i, rss_url in enumerate(rss_urls):
        try:
            feed = feedparser.parse(rss_url)
            channel_title = feed.feed.title if 'title' in feed.feed else 'RSS feed'
            if feed.entries:
                entry = feed.entries[0]
            else:
                print("No new entries in the feed.")  # 防止因长期RSS源无新内容，导致loop崩溃
                continue
            if entry.link != prev_entry_links[i]:
                prev_entry_links[i] = entry.link
                channel = bot.get_channel(CHANNAL_ID)  # 这里写入频道ID
                description_html = html.fromstring(entry.description)

                # 替换 <br> 标签为换行符
                for br in description_html.xpath('//br'):
                    br.tail = '\n' + br.tail if br.tail else '\n'

                description_text = ''.join(description_html.itertext())
                image_url = description_html.xpath('//img/@src')[0] if description_html.xpath('//img/@src') else ''
                message = f'{channel_title} 更新了：\n\n{description_text}\n\n{entry.link}\n\n{image_url}'
                await channel.send(message)
        except Exception as e:
            print(f"千夏现在不能更新这个RSS（{rss_url}）哦~")

