# Requests for API, Asyncio to call sleep() in async func
import requests
import asyncio

# Aiogram
from aiogram import Bot
from aiogram.types import ParseMode

# We also need config here
import db
import config
from datetime import datetime
import hmac
import base64 
import hashlib

async def start():

    # We need the Bot instance here to send deposit notifications to users
    bot = Bot(token=config.BOT_TOKEN)

    while True:
        # 2 Seconds delay between checks
        await asyncio.sleep(2)


        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        sign = hmac.new(config.API_SECRET_KEY, timestamp + 'GET' + f'/api/v5/finance/staking-defi/offers?protocolType=staking&ccy=TONCOIN', hashlib.sha256 ).encode("ascii") 
        resp = requests.get(f'{config.API_BASE_URL}/api/v5/finance/staking-defi/offers?'
                                f'protocolType=staking&'
                                f'ccy=TONCOIN', 
                                headers={
                                    "OK-ACCESS-KEY": f"{config.API_KEY}",
                                    "OK-ACCESS-SIGN": f'{sign}',
                                    "OK-ACCESS-TIMESTAMP": f'{timestamp}',
                                    "OK-ACCESS-PASSPHRASE": f"{config.API_PASSPHRASE}"              
                                         }).json()


        # Iterating over currencies
        for ccy in resp['data']:
            apy = ccy['apy']
            if apy >= 0.3:
                apy = apy * 100
                syb = ccy['ccy']
                uid_list = db.get_subscribers(syb)
                for uid in uid_list:
                    await bot.send_message(uid, f'[Rate Alert] {syb}\n\n Estimated rate for the next hour is: {apy}%', parse_mode=ParseMode.MARKDOWN)
