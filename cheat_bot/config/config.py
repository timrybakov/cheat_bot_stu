from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AUTH_TOKEN: str
    ADMIN_GROUP_ID: int
    TUNNEL_URL: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
db_settings = DBSettings()
