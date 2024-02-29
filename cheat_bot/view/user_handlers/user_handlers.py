from aiogram import types, Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from asyncpg import UniqueViolationError

from cheat_bot.model.fsm.storage import UserCallbackData
from cheat_bot.presenter.user_presenter.user_presenter import UserPresenter
from cheat_bot.view.keyboards.keyboards import get_on_start_keyboard, get_academic_year_keyboard
from cheat_bot.view.keyboards.callbacks import GetOrPostCallback
from cheat_bot.view.keyboards.enums import Action

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
    presenter.on_start_check_permission(message.chat.id)
    await presenter.get_fsm_storage.clear()
    await presenter.get_fsm_storage.set_state(UserCallbackData.start)
    await message.answer(
        text='Welcome to STU Cheat Bot',
        reply_markup=get_on_start_keyboard()
    )


@user_router.callback_query(
    StateFilter(UserCallbackData.start),
    GetOrPostCallback.filter(F.method == Action.post)
)
async def post_choosing_academic_year(
        query: types.CallbackQuery,
        state: FSMContext
) -> None:
    """Хэндлер запроса на добавление материала.

    Обрабатывает callback-запрос (post),
    устанавливает пользователя в состояние
    (academic_year) выбора года обучения.

    :param query:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    await presenter.get_fsm_storage.update_data(
        method=query.data.split(':')[1],
        username=query.from_user.username
    )
    await query.message.edit_text(
        text='Для отправки материала выберите год обучения:',
        inline_message_id=str(query.from_user.id),
        reply_markup=get_academic_year_keyboard()
    )
    await presenter.get_fsm_storage.set_state(UserCallbackData.academic_year)


@user_router.callback_query(
    StateFilter(UserCallbackData.start),
    GetOrPostCallback.filter(F.method == Action.get)
)
async def get_choosing_academic_year(
        query: types.CallbackQuery,
        state: FSMContext
) -> None:
    """Хэндлер запроса на получение материала.

    Обрабатывает callback-запрос (get),
    устанавливает пользователя в состояние
    (academic_year) выбора года обучения.

    :param query:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    await presenter.get_fsm_storage.update_data(
        method=query.data.split(':')[1],
        username=query.from_user.username
    )
    await query.message.edit_text(
        text='Для получения материала выберите год обучения:',
        inline_message_id=str(query.from_user.id),
        reply_markup=get_academic_year_keyboard()
    )
    await presenter.get_fsm_storage.set_state(
        UserCallbackData.academic_year
    )


@user_router.callback_query(
    StateFilter(UserCallbackData.academic_year)
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
    fsm_storage = await presenter.get_fsm_storage.get_data()
    await query.message.edit_text(
        text=(
            'Для продолжения работы введите данный о вашем'
            'обучении по шаблону: b-<направление_обучения>/b-<предмет>'
        ),
        inline_message_id=str(query.from_user.id)
    )
    await presenter.set_method(query, fsm_storage)


@user_router.message(StateFilter(UserCallbackData.get))
async def get_to_aws_storage(message: types.Message, bot: Bot, state: FSMContext):
    """Хэндлер получение сообщения от пользователя по шаблону.

    Обрабатывает запрос пользователя на получение
    всего материала по выбранному шаблону в хэндлере
    'major_command_line'.

    :param message:
    :param bot:
    :param state:
    :return:
    """
    presenter = UserPresenter(state)
    list_of_images, fsm_storage = await presenter.get_all_images(message)
    for image_url in list_of_images:
        await bot.send_photo(
            chat_id=fsm_storage.get('user_telegram_id'),
            photo=image_url,
            protect_content=True
        )
    else:
        await message.answer(
            text='Спасибо что используете бота.'
        )
        await presenter.get_fsm_storage.clear()


@user_router.message(StateFilter(UserCallbackData.post), F.text)
async def post_to_aws_storage(
        message: types.Message,
        bot: Bot, state: FSMContext
):
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
    await presenter.get_fsm_storage.update_data(file_path=message.text.lower())
    fsm_storage = await presenter.get_fsm_storage.get_data()
    await bot.send_message(
        chat_id=fsm_storage.get('user_telegram_id'),
        text='Отправьте пожалуйста материал.'
    )


@user_router.message(StateFilter(UserCallbackData.post), F.photo)
async def post_to_aws_storage(
        message: types.Message,
        bot: Bot, state: FSMContext
):
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
        await presenter.get_fsm_storage.update_data(
            image_id=message.photo[-1].file_id,
            file_unique_id=message.photo[-1].file_unique_id
        )
        fsm_storage = await presenter.get_fsm_storage.get_data()
        await presenter.post_image(**fsm_storage)
        await bot.send_message(
            chat_id=fsm_storage.get('user_telegram_id'),
            text=('Фотографии отправлены на проверку модераторам. ' 
                  'По окончании проверки мы Вас оповестим.'
                  )
        )
    except UniqueViolationError:
        await message.answer(
            text='Вы уже отправляли данный материал.'
        )
    except ValueError:
        await message.answer(
            text='Проверьте правильность заполнения шаблона.'
        )


@user_router.message(StateFilter(UserCallbackData.post))
async def post_wrong_material(
    message: types.Message
):
    """Хэндлер обработки посторонненого материал от пользователя.

    :param message:
    :return:
    """
    await message.answer(
        text='Бот пока поддерживает только фотографии со сжатием. Отправьте фото повторно.'
    )
