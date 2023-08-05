import os
import requests
import telegram
from telegram.ext import ContextTypes, Application
from telegram.request import HTTPXRequest
import asyncio
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

token = 'YOUR TOKEN'
chat_id = 'YOUR CHAT ID'
bot = telegram.Bot(token = token, request=HTTPXRequest(http_version='1.1'))
cur1_url = None
cur2_url = None

async def send_msg(up_url, up_title):
    await bot.send_message(chat_id,f'MESSAGE\n{up_title}\n{up_url}')
    print('Update Detected!')

async def callback(context: ContextTypes.DEFAULT_TYPE):
    url1='URL1'
    html1 = requests.get(url1, headers = header).text
    soup1 = BeautifulSoup(html1, 'html.parser')
    up1 = soup1.find('ELEMENT')
    up1_title = up1.text.strip()
    up1_url = f'URL1{up1["href"]}'

    url2='URL2'
    html2 = requests.get(url2, headers = header).text
    soup2 = BeautifulSoup(html2, 'html.parser')
    up2 = soup2.find('ELEMENT')
    up2_title = up2.text.strip()
    up2_url = f'URL2{up2["href"]}'

    global cur1_url, cur2_url

    if cur1_url != up1_url:
        cur1_url = up1_url
        asyncio.create_task(send_msg(up1_url, up1_title))
        if up1_url != up2_url: # URL1 solely updated
            pass
        else: # url1, url2 # Both url1 and url2 updated
            cur2_url = up2_url
    elif cur2_url != up2_url: # Url2 solely updated
        cur2_url = up2_url
        asyncio.create_task(send_msg(up2_url, up2_title))
    else: # No update
        print('No Update')

application = Application.builder().token(token).build()
application.job_queue.run_repeating(callback, interval=300)
application.run_polling()
