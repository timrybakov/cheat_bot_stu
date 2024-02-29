from pydantic import BaseModel, field_validator


class InsertValidator(BaseModel):
    username: str
    user_telegram_id: int
    bucket: str
    file_path: str
    image_id: str
    file_unique_id: str

    @field_validator('file_path')
    @classmethod
    def validate_file_path(cls, value: str):
        new_value = value.split('/')
        if '/' not in value or len(new_value) != 2:
            raise ValueError
        return value
