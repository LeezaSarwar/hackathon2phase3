from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    database_url: str
    better_auth_secret: str
    frontend_url: str = "https://todoagent.techkl.de"
    cors_origins: str = "https://todoagent.techkl.de"

    # Gemini Configuration
    gemini_api_key: str | None = None
    agent_model: str = "gemini-1.5-flash"
    max_conversation_messages: int = 50

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS string into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    settings = Settings()
    # Debug: Print the loaded model name
    print(f"\n{'='*60}")
    print(f"SETTINGS LOADED")
    print(f"Agent Model: {settings.agent_model}")
    print(f"Gemini API Key: {settings.gemini_api_key[:20]}..." if settings.gemini_api_key else "No API Key")
    print(f"{'='*60}\n")
    return settings
