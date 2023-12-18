# Requests for API, Asyncio to call sleep() in async func
import asyncio
import okx.Account as Account
from timeit import default_timer as timer

# Aiogram
from aiogram import Bot

# We also need config here
import db
import config

accountAPI = Account.AccountAPI(config.API_KEY, config.API_SECRET_KEY, config.API_PASSPHRASE, False, flag="0")

async def start():

    bot = Bot(token=config.BOT_TOKEN)

    while True:
        # 60 Seconds delay between checks
        start = timer()
        try:
            resp = accountAPI.get_interest_rate()
            uid_list = db.get_subscribers()
        except:
            continue
        alert = False
        msg = '[Rate Alert]'

        # Iterating over currencies
        for ccy in resp['data']:
            rate = float(ccy['interestRate']) * 876000
            if float(rate) >= 25:
                syb = ccy['ccy']         
                msg = msg + f'\n\n{syb}: Current borrowing rate is {rate}%'
                alert = True

        if alert:        
            for uid in uid_list:
                try:
                   await bot.send_message(uid, msg)
                except:
                    pass
        end = timer()
        await asyncio.sleep(300 - (end - start))