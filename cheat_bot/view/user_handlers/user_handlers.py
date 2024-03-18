from aiogram import types, F, Bot, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from cheat_bot.view import keyboards, templates
from cheat_bot.presenter import error_handlers
from cheat_bot.presenter.user_presenter import UserPresenter
from ...presenter.error_handlers import custom_errors

user_router = Router()


@user_router.message(Command('start'))
async def on_start(
        message: types.Message,
        state: FSMContext
) -> None:
    """Хэндлер старта взаимодействия с пользователем.

    :param message:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    await presenter.get_fsm_storage.clear()
    await presenter.get_fsm_storage.set_state(
        keyboards.UserCallbackData.start_conversation_state
    )
    await message.answer(
        text=f'{templates.text_data["user_handlers"]["on_start"]}',
        reply_markup=keyboards.get_on_start_keyboard()
    )


@user_router.callback_query(
    StateFilter(keyboards.UserCallbackData.start_conversation_state),
    keyboards.GetOrPostCallback.filter(
        F.method == keyboards.Action.post_interaction_method
    )
)
async def post_choosing_academic_year(
        query: types.CallbackQuery,
        state: FSMContext
) -> None:
    """Хэндлер запроса на добавление материала.

    Обрабатывает callback-запрос (post),
    устанавливает пользователя в состояние
    (choosing_academic_year_state) выбора года обучения.

    :param query:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    await presenter.get_fsm_storage.update(
        method=query.data.split(':')[1],
        username=query.from_user.username
    )
    await query.message.edit_text(
        text=f'{templates.text_data["user_handlers"]["post_choosing_academic_year"]}',
        inline_message_id=str(query.from_user.id),
        reply_markup=keyboards.get_academic_year_keyboard()
    )
    await presenter.get_fsm_storage.set_state(
        keyboards.UserCallbackData.choosing_academic_year_state
    )


@user_router.callback_query(
    StateFilter(keyboards.UserCallbackData.start_conversation_state),
    keyboards.GetOrPostCallback.filter(
        F.method == keyboards.Action.get_interaction_method
    )
)
async def get_choosing_academic_year(
        query: types.CallbackQuery,
        state: FSMContext
) -> None:
    """Хэндлер запроса на получение материала.

    Обрабатывает callback-запрос (get),
    устанавливает пользователя в состояние
    (choosing_academic_year_state) выбора года обучения.

    :param query:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    await presenter.get_fsm_storage.update(
        method=query.data.split(':')[1],
        username=query.from_user.username
    )
    await query.message.edit_text(
        text=f'{templates.text_data["user_handlers"]["get_choosing_academic_year"]}',
        inline_message_id=str(query.from_user.id),
        reply_markup=keyboards.get_academic_year_keyboard()
    )
    await presenter.get_fsm_storage.set_state(
        keyboards.UserCallbackData.choosing_academic_year_state
    )


@user_router.callback_query(
    StateFilter(keyboards.UserCallbackData.choosing_academic_year_state)
)
async def major_command_line(
        query: types.CallbackQuery,
        state: FSMContext
) -> None:
    """Хэндлер после выбора года обучения.

    Обрабатывает текстовую команду от пользователя,
    и изменяет состояние, в котором находится пользователь,
    в зависимости от выбора пользователем (post или get) callback-ответа.

    :param query:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    fsm_storage = await presenter.get_fsm_storage.get()
    await query.message.edit_text(
        text=f'{templates.text_data["user_handlers"]["file_path_template"]}',
        inline_message_id=str(query.from_user.id)
    )
    if fsm_storage.get('method') == 'post_interaction_method':
        await presenter.set_user_interaction_method(query, fsm_storage)
        await presenter.get_fsm_storage.set_state(
            keyboards.UserCallbackData.posting_data_state
        )
    else:
        await presenter.set_user_interaction_method(query, fsm_storage)
        await presenter.get_fsm_storage.set_state(
            keyboards.UserCallbackData.getting_data_state
        )


@user_router.message(StateFilter(keyboards.UserCallbackData.getting_data_state))
async def get_to_aws_storage(
        message: types.Message,
        bot: Bot, state: FSMContext
) -> None:
    """Хэндлер получение сообщения от пользователя по шаблону.

    Обрабатывает запрос пользователя на получение
    всего материала по выбранному шаблону в хэндлере
    'major_command_line'.

    :param message:
    :param bot:
    :param state:
    :return:
    """
    try:
        presenter = UserPresenter(state)
        list_of_images, fsm_storage = await presenter.get_all_images(message)
        for image_url in list_of_images:
            await bot.send_photo(
                chat_id=fsm_storage.get('telegram_id'),
                photo=image_url,
                protect_content=True
            )
        else:
            await message.answer(
                text=f'{templates.text_data["user_handlers"]["thanks"]}'
            )
            await presenter.get_fsm_storage.clear()
    except error_handlers.ClientS3exception:
        await message.answer(
            text=f'{templates.text_data["user_handlers"]["server_error"]}'
        )


@user_router.message(StateFilter(keyboards.UserCallbackData.posting_data_state), F.text)
async def post_to_aws_storage(
        message: types.Message,
        bot: Bot, state: FSMContext
) -> None:
    """Хэндлер получение сообщения от пользователя по шаблону.

    Обрабатывает запрос пользователя на добавление
    материала по выбранному шаблону в хэндлере
    'major_command_line'.

    :param message:
    :param bot:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    await presenter.get_fsm_storage.update(file_path=message.text.lower())
    fsm_storage = await presenter.get_fsm_storage.get()
    await bot.send_message(
        chat_id=fsm_storage.get('telegram_id'),
        text=f'{templates.text_data["user_handlers"]["post_to_aws_storage"]}'
    )


@user_router.message(StateFilter(keyboards.UserCallbackData.posting_data_state), F.photo)
async def post_to_aws_storage_photo(
        message: types.Message,
        bot: Bot, state: FSMContext
) -> None:
    """Хэндлер получение материала от пользователя.

    Обрабатывает материал, отправленный пользователем, и
    добавляет материал в БД для последующей проверки модератором.

    :param message:
    :param bot:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    try:
        await presenter.get_fsm_storage.update(
            image_id=message.photo[-1].file_id,
            file_id=message.photo[-1].file_unique_id
        )
        fsm_storage = await presenter.get_fsm_storage.get()
        await presenter.post_image(fsm_storage)
        await bot.send_message(
            chat_id=fsm_storage.get('telegram_id'),
            text=f'{templates.text_data["user_handlers"]["sending_to_moderators"]}'
        )
    except custom_errors.NotUniqueException:
        await message.answer(
            text=f'{templates.text_data["user_handlers"]["sending_again"]}'
        )
    except custom_errors.AfterValidationException:
        await message.answer(
            text=f'{templates.text_data["user_handlers"]["incorrect_path"]}'
        )


@user_router.message(StateFilter(keyboards.UserCallbackData.posting_data_state))
async def post_wrong_material(
    message: types.Message
) -> None:
    """Хэндлер обработки посторонненого материал от пользователя.

    :param message:
    :return:
    """
    await message.answer(
        text=f'{templates.text_data["user_handlers"]["post_wrong_material"]}'
    )
