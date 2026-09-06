"""
config.py — Centralised application configuration.

Loads every setting from environment variables (populated via .env by
python-dotenv) so no secrets are hard-coded in source.
"""

import os
from dotenv import load_dotenv

# Load .env file at import time so all os.getenv() calls below resolve correctly
load_dotenv()


class Config:
    """Base configuration shared by all environments."""

    # ------------------------------------------------------------------ #
    #  Flask                                                               #
    # ------------------------------------------------------------------ #
    SECRET_KEY: str = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-in-prod")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    HOST: str = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("FLASK_PORT", "5000"))

    # ------------------------------------------------------------------ #
    #  IBM watsonx.ai                                                      #
    # ------------------------------------------------------------------ #
    WATSONX_API_KEY: str = os.getenv("WATSONX_API_KEY", "")
    WATSONX_URL: str = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    WATSONX_PROJECT_ID: str = os.getenv("WATSONX_PROJECT_ID", "")
    WATSONX_MODEL_ID: str = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-3-8b-instruct")

    # ------------------------------------------------------------------ #
    #  Model inference parameters                                          #
    # ------------------------------------------------------------------ #
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1024"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

    # ------------------------------------------------------------------ #
    #  Application metadata                                                #
    # ------------------------------------------------------------------ #
    APP_NAME: str = os.getenv("APP_NAME", "Smart Farming Advice Agent")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Map string names to config objects for easy selection
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

# Active config — defaults to development if FLASK_ENV is not set
active_config = config_map.get(os.getenv("FLASK_ENV", "development"), DevelopmentConfig)
