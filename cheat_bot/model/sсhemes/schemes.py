from pydantic import BaseModel, field_validator

from .constants import CHECK_FILE_PATH_CONSTANT


class UserScheme(BaseModel):
    username: str
    telegram_id: int
    academy_year: str
    file_path: str
    image_id: str
    file_id: str

    @field_validator('file_path')
    @classmethod
    def validate_file_path(cls, value: str):
        new_value = value.split('/')
        if '/' not in value or len(new_value) != CHECK_FILE_PATH_CONSTANT:
            raise ValueError
        return value
