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
        self._api_key: str = ""
        self._project_id: str = ""

    # ------------------------------------------------------------------ #
    #  Initialisation                                                      #
    # ------------------------------------------------------------------ #
    def initialise(self) -> None:
        """
        Connect to IBM watsonx.ai. Always re-reads credentials from the
        .env file so stale in-memory values never cause auth failures.
        If already initialised with the same key, reuses the connection.
        """
        import os
        from dotenv import load_dotenv
        # Force reload .env every time so the latest credentials are used
        load_dotenv(
            dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'),
            override=True,
        )

        api_key    = os.environ.get("WATSONX_API_KEY", "")
        project_id = os.environ.get("WATSONX_PROJECT_ID", "")
        url        = os.environ.get("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        model_id   = os.environ.get("WATSONX_MODEL_ID", "ibm/granite-4-h-small")

        # Re-initialise if credentials have changed since last init
        if self._initialised and self._api_key == api_key and self._project_id == project_id:
            return

        # Reset state before attempting new connection
        self._initialised = False
        self._model = None

        if not api_key:
            raise ValueError(
                "WATSONX_API_KEY is not set. "
                "Add it to your .env file and restart the server."
            )
        if not project_id:
            raise ValueError(
                "WATSONX_PROJECT_ID is not set. "
                "Add it to your .env file and restart the server."
            )

        credentials = Credentials(api_key=api_key, url=url)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self._model = ModelInference(
                model_id=model_id,
                credentials=credentials,
                project_id=project_id,
                params={
                    GenParams.MAX_NEW_TOKENS: int(os.environ.get("MAX_TOKENS", "1024")),
                    GenParams.TEMPERATURE: float(os.environ.get("TEMPERATURE", "0.7")),
                    GenParams.REPETITION_PENALTY: 1.1,
                },
            )

        self._api_key    = api_key
        self._project_id = project_id
        self._initialised = True
        logger.info("WatsonxClient initialised — model: %s  project: %s", model_id, project_id)

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
        import os
        try:
            self.initialise()
            return {
                "status": "connected",
                "model": os.environ.get("WATSONX_MODEL_ID", "ibm/granite-4-h-small"),
                "url":   os.environ.get("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
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
