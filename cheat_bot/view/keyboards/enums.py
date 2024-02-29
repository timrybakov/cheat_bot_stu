from enum import Enum


class Action(str, Enum):
    post = 'post'
    get = 'get'


class AdminAccess(str, Enum):
    accept = 'accept'
    reject = 'reject'


class AcademicTerm(str, Enum):
    first_year = 'first-year-study'
    second_year = 'second-year-study'
    third_year = 'third-year-study'
