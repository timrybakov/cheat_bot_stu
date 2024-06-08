from enum import Enum


class Action(str, Enum):
    post_interaction_method = 'post_interaction_method'
    get_interaction_method = 'get_interaction_method'


class AdminAccess(str, Enum):
    accept = 'accept'
    reject = 'reject'


class AcademicTerm(str, Enum):
    first_year = 'first-year-study'
    second_year = 'second-year-study'
    third_year = 'third-year-study'


class Buttons(Enum):
    accept_button = '✅'
    reject_button = '❌'
    first_year = '1'
    second_year = '2'
    third_year = '3'
    get_materials = 'Получить материалы'
    post_materials = 'Добавить материалы'
