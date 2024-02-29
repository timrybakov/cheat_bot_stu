from aiogram.filters.callback_data import CallbackData

from .enums import Action, AcademicTerm, AdminAccess


class GetOrPostCallback(CallbackData, prefix='first_callback'):
    method: Action


class AcademicTermCallback(CallbackData, prefix='academic_term'):
    academy_year: AcademicTerm


class AdminAccessCallback(CallbackData, prefix='admin_access'):
    admin_access: AdminAccess
