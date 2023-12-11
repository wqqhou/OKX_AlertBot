# Requests for API, Asyncio to call sleep() in async func
import asyncio
import okx.Account as Account

# Aiogram
from aiogram import Bot
from aiogram.types import ParseMode

# We also need config here
import db
import config

accountAPI = Account.AccountAPI(config.API_KEY, config.API_SECRET_KEY, config.API_PASSPHRASE, False, flag="0")

async def start():

    # We need the Bot instance here to send deposit notifications to users
    bot = Bot(token=config.BOT_TOKEN)

    while True:
        # 2 Seconds delay between checks
        asyncio.sleep(60)
        resp = accountAPI.get_interest_rate(ccy = "TON")

        # Iterating over currencies
        for ccy in resp['data']:
            rate = float(ccy['interestRate']) * 876000
            if float(rate) >= 30:
                syb = ccy['ccy']
                uid_list = db.get_subscribers(syb)
                for uid in uid_list:
                    try:
                       await bot.send_message(uid, f'[Rate Alert] {syb}\n\n Current borrowing rate is: {rate}%', parse_mode=ParseMode.MARKDOWN)
                    except:
                        pass