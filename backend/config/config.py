from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "Secret_Key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite+aiosqlite:///app.db"
    DEFAULT_USER_PROFILE_PIC: str = "default_media/default.png"
    PROFILE_PICTURES_PATH: str = "media/users"
    
    OAUTH_GOOGLE_CLIENT_ID: str = "google_client_id"
    OAUTH_GOOGLE_CLIENT_SECRET: str = "google_client_secret"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()