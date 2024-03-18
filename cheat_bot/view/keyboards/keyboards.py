from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callbacks import GetOrPostCallback, AcademicTermCallback, AdminAccessCallback
from .enums import AdminAccess, Action, AcademicTerm, Buttons


def get_on_start_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=Buttons.get_materials.value,
                callback_data=GetOrPostCallback(method=Action.get_interaction_method).pack()
            )
        ],
            [
                InlineKeyboardButton(
                    text=Buttons.post_materials.value,
                    callback_data=GetOrPostCallback(method=Action.post_interaction_method).pack()
                )
            ]
        ]
    )
    return inline_keyboard


def get_academic_year_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=Buttons.first_year.value,
                callback_data=AcademicTermCallback(
                    academy_year=AcademicTerm.first_year
                ).pack()
            )
        ],
            [
                InlineKeyboardButton(
                    text=Buttons.second_year.value,
                    callback_data=AcademicTermCallback(
                        academy_year=AcademicTerm.second_year
                    ).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=Buttons.third_year.value,
                    callback_data=AcademicTermCallback(
                        academy_year=AcademicTerm.third_year
                    ).pack()
                )
            ],
        ]
    )
    return inline_keyboard


def get_admin_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=Buttons.accept_button.value,
                callback_data=AdminAccessCallback(admin_access=AdminAccess.accept).pack()
            ),
            InlineKeyboardButton(
                text=Buttons.reject_button.value,
                callback_data=AdminAccessCallback(admin_access=AdminAccess.reject).pack()
            )
        ]]
    )
    return inline_keyboard
