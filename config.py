"""
config.py — Centralised application configuration.

Loads every setting from environment variables (populated via .env by
python-dotenv) so no secrets are hard-coded in source.
"""

import os
from dotenv import load_dotenv

# Always reload .env from disk — override any previously set env vars
# so stale values from a previous process never persist.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"), override=True)


class Config:
    """Base configuration — reads directly from os.environ at access time."""

    # ------------------------------------------------------------------ #
    #  Flask                                                               #
    # ------------------------------------------------------------------ #
    @property
    def SECRET_KEY(self) -> str:        return os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-in-prod")
    @property
    def DEBUG(self) -> bool:            return os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    @property
    def HOST(self) -> str:              return os.environ.get("FLASK_HOST", "0.0.0.0")
    @property
    def PORT(self) -> int:              return int(os.environ.get("FLASK_PORT", "5000"))

    # ------------------------------------------------------------------ #
    #  IBM watsonx.ai                                                      #
    # ------------------------------------------------------------------ #
    @property
    def WATSONX_API_KEY(self) -> str:     return os.environ.get("WATSONX_API_KEY", "")
    @property
    def WATSONX_URL(self) -> str:         return os.environ.get("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    @property
    def WATSONX_PROJECT_ID(self) -> str:  return os.environ.get("WATSONX_PROJECT_ID", "")
    @property
    def WATSONX_MODEL_ID(self) -> str:    return os.environ.get("WATSONX_MODEL_ID", "ibm/granite-4-h-small")

    # ------------------------------------------------------------------ #
    #  Model inference parameters                                          #
    # ------------------------------------------------------------------ #
    @property
    def MAX_TOKENS(self) -> int:        return int(os.environ.get("MAX_TOKENS", "1024"))
    @property
    def TEMPERATURE(self) -> float:     return float(os.environ.get("TEMPERATURE", "0.7"))

    # ------------------------------------------------------------------ #
    #  Application metadata                                                #
    # ------------------------------------------------------------------ #
    @property
    def APP_NAME(self) -> str:          return os.environ.get("APP_NAME", "Smart Farming Advice Agent")
    @property
    def APP_VERSION(self) -> str:       return os.environ.get("APP_VERSION", "1.0.0")


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


# Map string names to config objects for easy selection
config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
}

# Active config instance — reads fresh env vars on every property access
active_config = config_map.get(os.environ.get("FLASK_ENV", "development"), DevelopmentConfig)()
