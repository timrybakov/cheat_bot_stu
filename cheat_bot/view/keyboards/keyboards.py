from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callbacks import GetOrPostCallback, AcademicTermCallback, AdminAccessCallback
from .enums import AdminAccess, Action, AcademicTerm


def get_on_start_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='Добавить материалы',
                callback_data=GetOrPostCallback(method=Action.post).pack()
            )],
            [InlineKeyboardButton(
                text='Получить материалы',
                callback_data=GetOrPostCallback(method=Action.get).pack()
            )]
        ]
    )
    return inline_keyboard


def get_academic_year_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='1',
                callback_data=AcademicTermCallback(
                    academy_year=AcademicTerm.first_year
                ).pack()
            )],
            [InlineKeyboardButton(
                text='2',
                callback_data=AcademicTermCallback(
                    academy_year=AcademicTerm.second_year
                ).pack()
            )],
            [InlineKeyboardButton(
                text='3',
                callback_data=AcademicTermCallback(
                    academy_year=AcademicTerm.third_year
                ).pack()
            )],
        ]
    )
    return inline_keyboard


def get_admin_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
                text='✅',
                callback_data=AdminAccessCallback(admin_access=AdminAccess.accept).pack()
            ),
            InlineKeyboardButton(
                text='❌',
                callback_data=AdminAccessCallback(admin_access=AdminAccess.reject).pack()
            )
        ]]
    )

    return inline_keyboard
