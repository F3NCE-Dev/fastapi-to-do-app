from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    SECRET_KEY: str = "Secret_Key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = "sqlite+aiosqlite:///backend/app.db"

    DEFAULT_USER_PROFILE_PIC_DIR: str = "backend/default_media"
    DEFAULT_USER_PROFILE_PIC_IMAGE: str = "default.png"
    MEDIA_DIR: str = "backend/media"
    
    FRONTEND_ORIGINS: list[str] = ["http://localhost:5500", "http://127.0.0.1:5500"]
    REDIRECT_URI: str = "http://localhost:5500/frontend/index.html"
    
    OAUTH_GOOGLE_CLIENT_ID: str = "google_client_id"
    OAUTH_GOOGLE_CLIENT_SECRET: str = "google_client_secret"

    OAUTH_GITHUB_CLIENT_ID: str = "github_client_id"
    OAUTH_GITHUB_CLIENT_SECRET: str = "github_client_secret"

    DEBUG_MODE: bool = True

    @property
    def DEFAULT_USER_PROFILE_PIC_URL(self) -> str:
        return f"{self.DEFAULT_USER_PROFILE_PIC_DIR}/{self.DEFAULT_USER_PROFILE_PIC_IMAGE}"

    @property
    def PROFILE_PICTURES_PATH(self) -> Path:
        return Path(self.MEDIA_DIR) / "users"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()