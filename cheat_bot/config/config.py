from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str


class Settings(BaseSettings):
    auth_token: str
    admin_group_id: int
    tunnel_url: str
    admins_id: str
    db_settings: DBSettings = DBSettings()
