# Requests for API, Asyncio to call sleep() in async func
import asyncio
import okx.Account as Account
import okx.PublicData as Public
from timeit import default_timer as timer

# Aiogram
from aiogram import Bot

# We also need config here
import db
import config

accountAPI = Account.AccountAPI(config.API_KEY, config.API_SECRET_KEY, config.API_PASSPHRASE, False, flag="0")
publicAPI = Public.PublicAPI(config.API_KEY, config.API_SECRET_KEY, config.API_PASSPHRASE, False, flag="0")


async def start():

    bot = Bot(token=config.BOT_TOKEN)

    while True:
        # 60 Seconds delay between checks
        start = timer()
        try:
            resp_i = accountAPI.get_interest_rate()
            resp_f = publicAPI.get_funding_rate()
            uid_list = db.get_subscribers()
        except:
            continue
        alert = False
        msg = '[Rate Alert]'

        info: dict = {}

        for inst in resp_f['data']:
            rate = float(inst['nextFundingRate']) * 100
            syb = inst['instrumentId'].split('-')[0]
            info[syb]: list = rate

        for ccy in resp_i['data']:
            rate = float(ccy['interestRate']) * 876000
            syb = ccy['ccy']         
            info[syb].append(rate)

        for syb in info:
            if info[syb][0] > 0.04 or info[syb][1] > 25:
                alert = True
                msg += f'\n\n{syb} Interest Rate: {info[syb][1]} Funding Rate: {info[syb][0]}%'

        if alert:        
            for uid in uid_list:
                try:
                   await bot.send_message(uid, msg)
                except:
                    pass

        end = timer()
        
        await asyncio.sleep(300 - (end - start))