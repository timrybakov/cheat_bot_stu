import logging

from aiogram import types, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F
from botocore import exceptions

from cheat_bot.model.fsm.storage import AdminCallbackData
from cheat_bot.presenter.user_presenter.user_presenter import UserPresenter
from cheat_bot.view.keyboards.callbacks import AdminAccessCallback
from cheat_bot.view.keyboards.keyboards import get_admin_keyboard
from cheat_bot.view.keyboards.enums import AdminAccess

admin_router = Router()

ADMIN = [689970990]


@admin_router.message(StateFilter(None), Command('admin'))
async def control_rights(message: types.Message, state: FSMContext):
    """Хэндлер команды - '/admin'.

    Проверяет наличие прав доступа для модерации сообщений.

    :param message:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    if message.from_user.id in ADMIN:
        await presenter.get_fsm_storage.set_state(AdminCallbackData.admin)
        await message.answer(
            text='Вы являетесь администратором, добро пожаловать в панель администратора.'
        )
    else:
        await message.answer(text='Вы обычный пользователь, у вас нет доступа к панели администратора.')


@admin_router.message(Command('cancel_admin'))
async def cancel_admin_no_state(message: types.Message, state: FSMContext):
    """Хэндлер команды - '/cancel_admin'.

    Сбрасывает данные состояния.

    :param message:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    if message.from_user.id in ADMIN:
        await presenter.get_fsm_storage.clear()
        await message.answer(
            text='Для повторного доступа к модерированию введите команду - /admin'
        )


@admin_router.message(
    StateFilter(AdminCallbackData.admin),
    Command('moderate'), F.text
)
async def moderate_image(
        message: types.Message,
        bot: Bot, state: FSMContext
):
    """Хэндлер команды - '/moderate'.

    Обрабатывает команду и отправляет фото
    для модерации.

    :param message:
    :param bot:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    try:
        user_data = await presenter.select_and_delete_from_database()
        await presenter.get_fsm_storage.update_data(**user_data)
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=user_data.image_id,
            reply_markup=get_admin_keyboard()
        )
    except AttributeError as error:
        logging.error(error)
        await message.answer(
            text='Материала для модерации пока нет.'
        )


@admin_router.callback_query(
    StateFilter(AdminCallbackData.admin),
    AdminAccessCallback.filter(F.admin_access == AdminAccess.accept)
)
async def accept_image(
        query: types.CallbackQuery,
        bot: Bot, state: FSMContext

):
    """Хэндлер добавление материала.

    Обрабатывает callback-запрос (accept),
    и добавляет материал в БД.

    :param query:
    :param bot:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    fsm_storage = await presenter.get_fsm_storage.get_data()
    try:
        presenter.send_to_s3_storage(
            fsm_storage.get('image_id'),
            fsm_storage.get('bucket'),
            fsm_storage.get('file_path')
        )
        await query.answer(
            text='Материал добавлен.'
        )
        await query.message.delete()
        await bot.send_message(
            chat_id=fsm_storage.get('user_telegram_id'),
            text='Фото проверено и добавлено в архив, спасибо что пользуетесь ботом.'
        )
        await presenter.get_fsm_storage.set_data({})
    except exceptions.ClientError as error:
        logging.error(error)
        await bot.send_message(
            chat_id=fsm_storage.get('user_id'),
            text='Проверьте правильность введенных данных по шаблону: ' + fsm_storage.get("file_path")
        )


@admin_router.callback_query(
    StateFilter(AdminCallbackData.admin),
    AdminAccessCallback.filter(F.admin_access == AdminAccess.reject)
)
async def reject_image(
        query: types.CallbackQuery,
        bot: Bot, state: FSMContext
):
    """Хэндлер отклонение материала.

    Обрабатывает callback-запрос (reject),
    и отклоняет запрос на добавление в БД.

    :param query:
    :param bot:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    fsm_storage = await presenter.get_fsm_storage.get_data()
    await query.answer(
        text='Материал отклонен.'
    )
    await query.message.delete()
    await bot.send_message(
        chat_id=fsm_storage.get('user_id'),
        text='Извините, но ваше фото не прошло модерацию.'
    )
    await presenter.get_fsm_storage.set_data({})
