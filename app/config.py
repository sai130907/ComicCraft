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
        "gemini-3.5-flash",
    )

    GEMINI_PRO_MODEL = os.getenv(
        "GEMINI_PRO_MODEL",
        "gemini-3.1-pro-preview",
    )

    IMAGE_MODEL = os.getenv(
        "IMAGE_MODEL",
        "black-forest-labs/FLUX.1-schnell",
    )

    # Hugging Face provider
    HF_PROVIDER = os.getenv(
        "HF_PROVIDER",
        "auto",
    )

    # Demo mode
    MOCK_MODE = os.getenv(
        "MOCK_MODE",
        "false",
    ).lower() == "true"

    # Comic settings
    PANEL_COUNT = 5

    # Application folders
    STATIC_DIR = "static"
    TEMPLATE_DIR = "templates"
    PANEL_DIR = "static/panels"
    EXPORT_DIR = "static/exports"


settings = Settings()