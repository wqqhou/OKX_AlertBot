# Requests for API, Asyncio to call sleep() in async func
import asyncio
import okx.Earning as Earning

# Aiogram
from aiogram import Bot
from aiogram.types import ParseMode

# We also need config here
import db
import config

async def start():

    # We need the Bot instance here to send deposit notifications to users
    bot = Bot(token=config.BOT_TOKEN)

    while True:
        # 2 Seconds delay between checks
        await asyncio.sleep(20)
        EarningAPI = Earning.EarningAPI(config.API_KEY, config.API_SECRET_KEY, config.API_PASSPHRASE, False, flag="0")
        syb = "BTC"
        resp = EarningAPI.get_offers(ccy = syb)
        print(resp)

        # Iterating over currencies
        for ccy in resp['data']:
            apy = ccy['apy']
            if apy >= 0.3:
                apy = apy * 100
                syb = ccy['ccy']
                uid_list = db.get_subscribers(syb)
                for uid in uid_list:
                    await bot.send_message(uid, f'[Rate Alert] {syb}\n\n Estimated rate for the next hour is: {apy}%', parse_mode=ParseMode.MARKDOWN)
