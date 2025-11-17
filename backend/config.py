import os


class Settings:
    """
    Simple settings class to hold API configuration for the AI IDE backend.  The
    values can be overridden by environment variables at runtime.  When you
    deploy this service locally via Electron the default values will be used
    unless you set the appropriate environment variables.
    """
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4.1-mini")


settings = Settings()
