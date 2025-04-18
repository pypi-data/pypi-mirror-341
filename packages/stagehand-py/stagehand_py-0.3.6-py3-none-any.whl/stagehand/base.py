import logging
import os
from abc import ABC, abstractmethod
from collections.abc import Awaitable
from typing import Any, Callable, Optional

from browserbase.types import SessionCreateParams as BrowserbaseSessionCreateParams

from .config import StagehandConfig
from .page import StagehandPage
from .utils import default_log_handler

logger = logging.getLogger(__name__)


class StagehandBase(ABC):
    """
    Base class for Stagehand client implementations.
    Defines the common interface and functionality for both sync and async versions.
    """

    def __init__(
        self,
        config: Optional["StagehandConfig"] = None,
        server_url: Optional[str] = None,
        session_id: Optional[str] = None,
        browserbase_api_key: Optional[str] = None,
        browserbase_project_id: Optional[str] = None,
        model_api_key: Optional[str] = None,
        on_log: Optional[
            Callable[[dict[str, Any]], Awaitable[None]]
        ] = default_log_handler,
        verbose: int = 1,
        model_name: Optional[str] = None,
        dom_settle_timeout_ms: Optional[int] = None,
        timeout_settings: Optional[Any] = None,
        stream_response: Optional[bool] = None,
        model_client_options: Optional[dict[str, Any]] = None,
        self_heal: Optional[bool] = None,
        wait_for_captcha_solves: Optional[bool] = None,
        system_prompt: Optional[str] = None,
        browserbase_session_create_params: Optional[
            BrowserbaseSessionCreateParams
        ] = None,
        enable_caching: Optional[bool] = None,
    ):
        """
        Initialize the Stagehand client with common configuration.

        Args:
            config (Optional[StagehandConfig]): Configuration object that can provide all settings.
            server_url (Optional[str]): URL of the Stagehand server.
            session_id (Optional[str]): Existing session ID to resume.
            browserbase_api_key (Optional[str]): Browserbase API key.
            browserbase_project_id (Optional[str]): Browserbase project ID.
            model_api_key (Optional[str]): Model provider API key.
            on_log (Optional[Callable]): Callback for log events.
            verbose (int): Verbosity level.
            model_name (Optional[str]): Name of the model to use.
            dom_settle_timeout_ms (Optional[int]): Time for DOM to settle in ms.
            debug_dom (Optional[bool]): Whether to enable DOM debugging.
            timeout_settings (Optional[float]): Request timeout in seconds.
            stream_response (Optional[bool]): Whether to stream responses.
            model_client_options (Optional[dict]): Options for the model client.
            self_heal (Optional[bool]): Whether to enable self-healing.
            wait_for_captcha_solves (Optional[bool]): Whether to wait for CAPTCHA solves.
            act_timeout_ms (Optional[int]): Timeout for act commands in ms.
            system_prompt (Optional[str]): System prompt for LLM interactions.
            browserbase_session_create_params (Optional[BrowserbaseSessionCreateParams]): Params for Browserbase session creation.
            enable_caching (Optional[bool]): Whether to enable caching functionality.
        """
        self.server_url = server_url or os.getenv("STAGEHAND_SERVER_URL")

        if config:
            self.browserbase_api_key = (
                config.api_key
                or browserbase_api_key
                or os.getenv("BROWSERBASE_API_KEY")
            )
            self.browserbase_project_id = (
                config.project_id
                or browserbase_project_id
                or os.getenv("BROWSERBASE_PROJECT_ID")
            )
            self.session_id = config.browserbase_session_id or session_id
            self.model_name = config.model_name or model_name
            self.dom_settle_timeout_ms = (
                config.dom_settle_timeout_ms or dom_settle_timeout_ms
            )
            self.self_heal = (
                config.self_heal if config.self_heal is not None else self_heal
            )
            self.wait_for_captcha_solves = (
                config.wait_for_captcha_solves
                if config.wait_for_captcha_solves is not None
                else wait_for_captcha_solves
            )
            self.system_prompt = config.system_prompt or system_prompt
            self.browserbase_session_create_params = (
                config.browserbase_session_create_params
                or browserbase_session_create_params
            )
            self.enable_caching = (
                config.enable_caching
                if config.enable_caching is not None
                else enable_caching
            )
            self.verbose = config.verbose if config.verbose is not None else verbose
        else:
            self.browserbase_api_key = browserbase_api_key or os.getenv(
                "BROWSERBASE_API_KEY"
            )
            self.browserbase_project_id = browserbase_project_id or os.getenv(
                "BROWSERBASE_PROJECT_ID"
            )
            self.session_id = session_id
            self.model_name = model_name
            self.dom_settle_timeout_ms = dom_settle_timeout_ms
            self.self_heal = self_heal
            self.wait_for_captcha_solves = wait_for_captcha_solves
            self.system_prompt = system_prompt
            self.browserbase_session_create_params = browserbase_session_create_params
            self.enable_caching = enable_caching
            self.verbose = verbose

        # Handle model-related settings directly
        self.model_api_key = model_api_key or os.getenv("MODEL_API_KEY")
        self.model_client_options = model_client_options or {}
        if self.model_api_key and "apiKey" not in self.model_client_options:
            self.model_client_options["apiKey"] = self.model_api_key

        # Handle streaming response setting directly
        self.streamed_response = (
            stream_response if stream_response is not None else True
        )

        self.on_log = on_log
        self.timeout_settings = timeout_settings or 180.0

        self._initialized = False
        self._closed = False
        self.page: Optional[StagehandPage] = None

        # Validate essential fields if session_id was provided
        if self.session_id:
            if not self.browserbase_api_key:
                raise ValueError(
                    "browserbase_api_key is required (or set BROWSERBASE_API_KEY in env)."
                )
            if not self.browserbase_project_id:
                raise ValueError(
                    "browserbase_project_id is required (or set BROWSERBASE_PROJECT_ID in env)."
                )

    @abstractmethod
    def init(self):
        """
        Initialize the Stagehand client.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Clean up resources.
        Must be implemented by subclasses.
        """
        pass
