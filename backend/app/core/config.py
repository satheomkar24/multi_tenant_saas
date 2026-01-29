import os
from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

# Load .env variables early
load_dotenv()

# Determine environment
ENV = os.getenv("ENV", "development")  # default to development

class Settings(BaseSettings):
    # ---------------- General ----------------
    ENV: str = Field(default="development", alias="ENV")
    APP_NAME: str = Field(default="MultiTenantSaaS", alias="APP_NAME")
    DEBUG: bool = Field(default=True, alias="DEBUG")
    CORS_ORIGINS: list[str] = Field(default_factory=list)

    # ---------------- MongoDB ----------------
    MONGO_URI: str = Field(default="mongodb://localhost:27017", alias="MONGO_URI")
    MONGO_DB_NAME: str = Field(default="multi_tenant_saas", alias="MONGO_DB_NAME")

    # ---------------- JWT / Auth ----------------
    JWT_SECRET: str = Field(default="supersecretjwtkey", alias="JWT_SECRET")
    JWT_ALGORITHM: str = Field(default="HS256", alias="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=3, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, alias="REFRESH_TOKEN_EXPIRE_DAYS")

    # ---------------- Redis / Background Jobs ----------------
    REDIS_URL: str | None = Field(default=None, alias="REDIS_URL")

    # ---------------- Config ----------------
    model_config = {
        "env_file": f".env.{ENV}" if os.path.exists(f".env.{ENV}") else ".env",
        "case_sensitive": True
    }

    # ---------------- Validators ----------------
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            # comma-separated string → list
            return [i.strip() for i in v.split(",")]
        return v

# Singleton instance for the app
settings = Settings()
