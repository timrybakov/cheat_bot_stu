import logging

import uvicorn as uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI
from redis.asyncio import Redis


from cheat_bot.config.config import settings
from cheat_bot.view.admin_handlers.admin_handlers import admin_router
from cheat_bot.view.user_handlers.user_handlers import user_router


WEBHOOK_PATH = f'/bot/{settings.AUTH_TOKEN}'
WEBHOOK_URL = settings.TUNNEL_URL + WEBHOOK_PATH

app = FastAPI()
bot = Bot(token=settings.AUTH_TOKEN)
redis = Redis()
dispatcher = Dispatcher(
    storage=RedisStorage(redis=redis)
)
dispatcher.include_router(admin_router)
dispatcher.include_router(user_router)


@app.on_event('startup')
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dispatcher.feed_update(bot=bot, update=telegram_update)


@app.on_event('shutdown')
async def on_shutdown():
    await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename=f'error_file.log',
        format=('%(asctime)s - [%(levelname)s] - %(name)s - '
                '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    )
    uvicorn.run(app, host='localhost', port=8000)
