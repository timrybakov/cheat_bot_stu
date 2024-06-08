import logging

from aiogram import types, Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from cheat_bot.view import keyboards, templates
from cheat_bot.presenter.user_presenter import UserPresenter
from cheat_bot.presenter import error_handlers
from .constants import ADMIN_LIST
from ...presenter.error_handlers.custom_errors import NoMaterialException

admin_router = Router()


@admin_router.message(Command('moderate'))
async def moderate_image(
        message: types.Message,
        bot: Bot, state: FSMContext
) -> None:
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
        if message.from_user.id in ADMIN_LIST:
            user_data = await presenter.get_first_obj()
            await presenter.get_fsm_storage.update(**dict(user_data))
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=user_data.image_id,
                reply_markup=keyboards.get_admin_keyboard()
            )
        else:
            await message.answer(
                text=f'{templates.text_data["admin_handlers"]["fake_admin"]}'
            )
    except NoMaterialException as error:
        logging.error(error)
        await message.answer(
            text=f'{templates.text_data["admin_handlers"]["moderation"]}'
        )


@admin_router.callback_query(
    keyboards.AdminAccessCallback.filter(
        F.admin_access == keyboards.AdminAccess.accept
    )
)
async def accept_image(
        query: types.CallbackQuery,
        bot: Bot, state: FSMContext

) -> None:
    """Хэндлер добавление материала.

    Обрабатывает callback-запрос (accept),
    и добавляет материал в БД.

    :param query:
    :param bot:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    fsm_storage = await presenter.get_fsm_storage.get()
    try:
        presenter.send_to_s3_storage(
            fsm_storage.get('image_id'),
            fsm_storage.get('academy_year'),
            fsm_storage.get('file_path')
        )
        await query.answer(
            text=f'{templates.text_data["admin_handlers"]["accept_image_admin_view"]}'
        )
        await query.message.delete()
        await bot.send_message(
            chat_id=fsm_storage.get('telegram_id'),
            text=f'{templates.text_data["admin_handlers"]["accept_image_user_view"]}'
        )
        await presenter.get_fsm_storage.set({})
    except error_handlers.ClientS3exception:
        await bot.send_message(
            chat_id=fsm_storage.get('telegram_id'),
            text=f'{templates.text_data["admin_handlers"]["incorrect_data"]} {fsm_storage.get("file_path")}'
        )


@admin_router.callback_query(
    keyboards.AdminAccessCallback.filter(
        F.admin_access == keyboards.AdminAccess.reject
    )
)
async def reject_image(
        query: types.CallbackQuery,
        bot: Bot, state: FSMContext
) -> None:
    """Хэндлер отклонение материала.

    Обрабатывает callback-запрос (reject),
    и отклоняет запрос на добавление в БД.

    :param query:
    :param bot:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    fsm_storage = await presenter.get_fsm_storage.get()
    await query.answer(
        text=f'{templates.text_data["admin_handlers"]["reject_image_admin_view"]}'
    )
    await query.message.delete()
    await bot.send_message(
        chat_id=fsm_storage.get('telegram_id'),
        text=f'{templates.text_data["admin_handlers"]["reject_image_user_view"]}'
    )
    await presenter.get_fsm_storage.set({})
