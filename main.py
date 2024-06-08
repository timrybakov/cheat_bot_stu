import logging

import uvicorn as uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI
from redis.asyncio import Redis


from cheat_bot import di, view


webhook_path = f'/bot/{di.di_container.settings.auth_token}'
webhook_url = di.di_container.settings.tunnel_url + webhook_path

app = FastAPI()
bot = Bot(token=di.di_container.settings.auth_token)
redis = Redis()
dispatcher = Dispatcher(
    storage=RedisStorage(redis=redis)
)
dispatcher.include_router(view.user_handlers.user_router)
dispatcher.include_router(view.admin_handlers.admin_router)


@app.on_event('startup')
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info != webhook_url:
        await bot.set_webhook(url=webhook_url)


@app.post(webhook_path)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dispatcher.feed_update(bot=bot, update=telegram_update)


@app.on_event('shutdown')
async def on_shutdown():
    await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=('%(asctime)s - [%(levelname)s] - %(name)s - '
                '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')
    )
    uvicorn.run(app, host='localhost', port=8000)
