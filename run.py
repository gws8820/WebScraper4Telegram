import sys
import os
import requests
import time
import telegram
import asyncio
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

async def main():
    token = 'YOUR_TOKEN'
    chat_id = YOUR_CHAT_ID
    bot = telegram.Bot(token = token)
    await bot.send_message(chat_id,f"MESSAGE")

while True:
    url='URL'
    html = requests.get(url, headers = header).text
    soup = BeautifulSoup(html, 'html.parser')
    
    up = soup.select('HTML_TAG')[]
    up_title = up.text.strip()
    up_dir = up['href']
    up_url = f'DOMAIN{up_dir}'

    with open(os.path.join(BASE_DIR, 'up_url.txt'), 'r+') as f:
        cur_url = f.readline()
        if cur_url != up_url:
            f.close()
            with open(os.path.join(BASE_DIR, 'up_url.txt'), 'w+') as f:
                f.write(up_url)
                f.close()
                print('Update Detected!')
            asyncio.run(main())
        else:
            f.close()
            print('No Update')
    
    time.sleep(600)
