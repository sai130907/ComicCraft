import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "ComicCraft"
    APP_VERSION = "1.0.0"

    # API keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    HF_TOKEN = os.getenv("HF_TOKEN", "")

    # AI models
    GEMINI_FLASH_MODEL = os.getenv(
        "GEMINI_FLASH_MODEL",
        "gemini-3.8-flash"
    )

    GEMINI_PRO_MODEL = os.getenv(
        "GEMINI_PRO_MODEL",
        "gemini-2.5-pro"
    )

    IMAGE_MODEL = os.getenv(
        "IMAGE_MODEL",
        "black-forest-labs/FLUX.1-schnell"
    )

    # Demo mode
    MOCK_MODE = os.getenv(
        "MOCK_MODE",
        "true"
    ).lower() == "true"

    # Comic settings
    PANEL_COUNT = 5

    # Application folders
    STATIC_DIR = "static"
    TEMPLATE_DIR = "templates"
    PANEL_DIR = "static/panels"
    EXPORT_DIR = "static/exports"


settings = Settings()