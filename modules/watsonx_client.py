"""
modules/watsonx_client.py

IBM watsonx.ai client wrapper.
Handles authentication, model initialisation, and chat/text generation
with the Granite model family.  All credentials come from config.py
(which reads from .env) — nothing is hard-coded here.
"""

from __future__ import annotations

import logging
import warnings

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

from config import active_config

logger = logging.getLogger(__name__)


class WatsonxClient:
    """
    Thin wrapper around ibm_watsonx_ai ModelInference that provides
    simple generate() and stream() methods used by the rest of the app.
    """

    def __init__(self) -> None:
        self._model: ModelInference | None = None
        self._initialised = False

    # ------------------------------------------------------------------ #
    #  Initialisation                                                      #
    # ------------------------------------------------------------------ #
    def initialise(self) -> None:
        """
        Lazily connect to the IBM watsonx.ai endpoint and load the model.
        Called on first use rather than at import time so the app can still
        start (and show config errors gracefully) if credentials are missing.
        """
        if self._initialised:
            return

        if not active_config.WATSONX_API_KEY:
            raise ValueError(
                "WATSONX_API_KEY is not set. "
                "Copy .env.example to .env and fill in your IBM Cloud API key."
            )
        if not active_config.WATSONX_PROJECT_ID:
            raise ValueError(
                "WATSONX_PROJECT_ID is not set. "
                "Copy .env.example to .env and fill in your watsonx.ai project ID."
            )

        credentials = Credentials(
            api_key=active_config.WATSONX_API_KEY,
            url=active_config.WATSONX_URL,
        )

        self._model = ModelInference(
            model_id=active_config.WATSONX_MODEL_ID,
            credentials=credentials,
            project_id=active_config.WATSONX_PROJECT_ID,
            params={
                GenParams.MAX_NEW_TOKENS: active_config.MAX_TOKENS,
                GenParams.TEMPERATURE: active_config.TEMPERATURE,
                GenParams.REPETITION_PENALTY: 1.1,
            },
        )
        # Suppress the deprecation warning for the older text/generation endpoint
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            module="ibm_watsonx_ai",
        )
        warnings.filterwarnings("ignore", message=".*deprecated.*", category=Warning)

        self._initialised = True
        logger.info("WatsonxClient initialised with model %s", active_config.WATSONX_MODEL_ID)

    # ------------------------------------------------------------------ #
    #  Text Generation                                                     #
    # ------------------------------------------------------------------ #
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Send a prompt to the Granite model and return the full response text.

        Args:
            prompt:        The user's message / question.
            system_prompt: Optional system instructions to prepend.

        Returns:
            Generated text string.
        """
        self.initialise()

        full_prompt = _build_prompt(system_prompt, prompt)

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                response = self._model.generate_text(prompt=full_prompt)  # type: ignore[union-attr]
            return response.strip() if response else "I'm sorry, I couldn't generate a response. Please try again."
        except Exception as exc:
            logger.error("watsonx generate error: %s", exc)
            raise

    # ------------------------------------------------------------------ #
    #  Chat (multi-turn)                                                   #
    # ------------------------------------------------------------------ #
    def chat(
        self,
        messages: list[dict],
        system_prompt: str = "",
    ) -> str:
        """
        Generate a response for a multi-turn conversation.

        Args:
            messages:      List of {"role": "user"|"assistant", "content": str}
            system_prompt: System instructions for this conversation.

        Returns:
            Generated text string.
        """
        self.initialise()

        full_prompt = _build_chat_prompt(system_prompt, messages)

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                response = self._model.generate_text(prompt=full_prompt)  # type: ignore[union-attr]
            return response.strip() if response else "I'm sorry, I couldn't generate a response. Please try again."
        except Exception as exc:
            logger.error("watsonx chat error: %s", exc)
            raise

    # ------------------------------------------------------------------ #
    #  Health check                                                        #
    # ------------------------------------------------------------------ #
    def health_check(self) -> dict:
        """Return status dict used by the /api/health endpoint."""
        try:
            self.initialise()
            return {
                "status": "connected",
                "model": active_config.WATSONX_MODEL_ID,
                "url": active_config.WATSONX_URL,
            }
        except Exception as exc:
            return {"status": "error", "message": str(exc)}


# ------------------------------------------------------------------ #
#  Private helpers                                                     #
# ------------------------------------------------------------------ #

def _build_prompt(system_prompt: str, user_prompt: str) -> str:
    """
    Format a single-turn prompt in Granite's recommended chat template.
    <|system|>…<|user|>…<|assistant|>
    """
    parts: list[str] = []
    if system_prompt:
        parts.append(f"<|system|>\n{system_prompt}\n<|end_of_text|>")
    parts.append(f"<|user|>\n{user_prompt}\n<|end_of_text|>")
    parts.append("<|assistant|>")
    return "\n".join(parts)


def _build_chat_prompt(system_prompt: str, messages: list[dict]) -> str:
    """
    Format a multi-turn conversation in Granite's chat template.
    Each message alternates role: user / assistant.
    """
    parts: list[str] = []
    if system_prompt:
        parts.append(f"<|system|>\n{system_prompt}\n<|end_of_text|>")

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            parts.append(f"<|user|>\n{content}\n<|end_of_text|>")
        elif role == "assistant":
            parts.append(f"<|assistant|>\n{content}\n<|end_of_text|>")

    parts.append("<|assistant|>")
    return "\n".join(parts)


# Module-level singleton — imported by app.py and other modules
watsonx_client = WatsonxClient()
