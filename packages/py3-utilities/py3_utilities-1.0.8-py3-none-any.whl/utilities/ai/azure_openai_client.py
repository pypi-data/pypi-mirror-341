import json
import logging
import time 
import tempfile
import os
import asyncio
import aiohttp
import openai

from typing import Optional, Dict, Union
from openai import AsyncAzureOpenAI

from ..utility_base import UtilityBase
from ..logger import Logger, LogWrapper


# Define exceptions
class OpenAIClientError(Exception):
    pass


class AzureOpenAIClient(UtilityBase):
    """
    A wrapper for interacting with Azure OpenAI.
    """
    SESSION_DIR = "sessions"

    def __init__(
            self, 
            azure_endpoint: str,
            api_key: str,
            api_version: str,
            llm_model: str,
            default_system_message: str = "You are a helpful assistant.",
            max_tokens: int = 4000,
            temperature: float = 0.0,
            top_p: float = 0.95,
            frequency_penalty: float = 0.0,
            presence_penalty: float = 0.0,
            include_message_history: bool = True,
            save_sessions_to_disk: bool = True,
            verbose: bool = False,
            log_messages: bool = False,
            logger: Optional[Union[logging.Logger | Logger | LogWrapper]] = None,
            log_level: Optional[int] = None
        ):
        """
        Initializes the LLMWrapper with the provided parameters.

        :param azure_endpoint: Azure endpoint URL.
        :param api_key: API key for Azure OpenAI.
        :param api_version: API version for Azure OpenAI.
        :param llm_model: The model name to use.
        :param system_message: Default system message to guide the LLM's behavior (default: 'You are a helpful assistant.').
        :param max_tokens: Maximum tokens for the response (default: 4000).
        :param temperature: Sampling temperature for randomness (default: 0.0).
        :param top_p: Probability for nucleus sampling (default: 0.95).
        :param frequency_penalty: Penalize repeated tokens (default: 0).
        :param presence_penalty: Penalize repeated topics (default: 0).
        :param include_message_history: Whether to include full history in requests (default: True).
        :param save_sessions_to_disk: Whether to backup the chat history onto the hard drive (default: True).
        :param verbose: If true debug messages are logged during the operations. Exceptions, Errors and Warnings are always logged.
        :param log_messages: If true messages and system messages are logged too.
        :param logger: Optional logger instance. If not provided, a default logger is used.
        :param log_level: Optional log level. If not provided INFO level will be used for logging
        """
        # Init base class
        super().__init__(verbose, logger, log_level)
        self.log_messages = log_messages

        # Validate required parameters
        self._validate_initialization_params(azure_endpoint, api_key, api_version, llm_model)

        # Set Azure OpenAI parameters
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.api_version = api_version
        self.llm_model = llm_model
        self.default_system_message = {"role": "system", "content": default_system_message}

        # Model configuration
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.include_message_history = include_message_history

        # Azure OpenAI Clients
        self.async_client = AsyncAzureOpenAI(azure_endpoint=azure_endpoint, api_key=api_key, api_version=api_version)

        # Initialize storage
        self.save_sessions_to_disk = save_sessions_to_disk
        if save_sessions_to_disk:
            os.makedirs(self.SESSION_DIR, exist_ok=True)
            self._load_all_sessions_from_disk()
        else:
            self.sessions = {}

        self._log(f"LLMWrapper initialized successfully. Conversation history {'enabled' if include_message_history else 'disabled'}.")
        self._log(f"Default system message: {default_system_message}")

    def request_completion(
            self, 
            message_content: str, 
            session_id: Optional[str] = None, 
            timeout: int = 30,
            retries: int = 3, 
            retry_delay: float = 2.0
        ) -> str:
        """
        Sends a new message to the LLM and retrieves the response with retry support.
        Do not use this function inside a running event loop.

        :param new_message_content: The user's message to send to the LLM.
        :param session_id: ID of the conversation session (default: None).
        :param timeout: Timeout for the API request (default: 30 seconds).
        :param retries: Number of retry attempts for transient failures (default: 3).
        :param retry_delay: Delay (in seconds) between retries (default: 2.0).
        :return: The LLM's response.
        """
        if not message_content.strip():
            raise ValueError("Message content cannot be empty.")

        # Request a completion, try it again "retries" times, if it fails
        for attempt in range(retries):
            try:
                response = asyncio.run(self._request_completion(message_content, session_id, timeout))
                return response
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {retry_delay * (2 ** attempt):.2f} seconds...")
                time.sleep(retry_delay * (2 ** attempt))

                if (attempt+1) == retries:
                    raise OpenAIClientError("Failed to complete the request after multiple retries.") from e

    async def request_completion_async(
            self, 
            message_content: str, 
            session_id: Optional[str] = None, 
            timeout: int = 30,
            retries: int = 3, 
            retry_delay: float = 2.0
        ) -> str:
        """
        Sends a new message to the LLM and retrieves the response with retry support asynchronously.

        :param new_message_content: The user's message to send to the LLM.
        :param session_id: ID of the conversation session (default: None).
        :param timeout: Timeout for the API request (default: 30 seconds).
        :param retries: Number of retry attempts for transient failures (default: 3).
        :param retry_delay: Delay (in seconds) between retries (default: 2.0).
        :return: The LLM's response.
        """
        if not message_content.strip():
            raise ValueError("Message content cannot be empty.")

        for attempt in range(retries):
            try:
                response = await self._request_completion(message_content, session_id, timeout)
                return response
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed. Retrying in {retry_delay * (2 ** attempt):.2f} seconds...")
                await asyncio.sleep(retry_delay * (2 ** attempt))

                if (attempt+1) == retries:
                    raise OpenAIClientError("Failed to complete the request after multiple retries.") from e

    def trim_conversation_history(self, session_id: Optional[str] = None, max_length: int = 50) -> None:
        """
        Trims the conversation history to the last `max_length` messages.

        :param session_id: ID of the conversation session (default: None).
        :param max_length: The maximum number of messages to retain in the history (default: 50).
        """
        if max_length <= 0:
            raise ValueError("`max_length` must be a positive integer.")

        session_id = self._validate_session(session_id)
        self._log(f"Trimming conversation history for session `{session_id}`")

        original_length = len(self.sessions[session_id])
        if original_length > max_length:
            self.sessions[session_id] = self.sessions[session_id][-max_length:]
            self._save_session_to_disk(session_id)

    def get_message_count(self, session_id: Optional[str] = None) -> int:
        """
        Gets the message count from the message history between the user and the LLM.

        :param session_id: ID of the conversation session (default: None).
        """
        session_id = self._validate_session(session_id)

        return len(self.sessions[session_id])

    def change_system_message(self, system_message: str, session_id: Optional[str] = None) -> None:
        """
        Changes the default system message.

        :param system_message: The new system message for the completion API.
        :param session_id: ID of the conversation session (default: None).
        """
        if not system_message.strip():
            raise ValueError("System message cannot be empty.")

        session_id = self._validate_session(session_id)

        if self.log_messages:
            self._log(f"Changing system message for session `{session_id}`. New system message: `{system_message}`")
        
        new_system_message: Dict[str, str] = {"role": "system", "content": system_message}
        self.sessions[session_id][0] = new_system_message

    def get_conversation_history_as_text(self, session_id: Optional[str] = None) -> str:
        """
        Returns the conversation history as a formatted plain text string.

        :param session_id: ID of the session (default: None).
        :return: The formatted conversation history as plain text.
        """
        session_id = self._validate_session(session_id)

        if not self.sessions[session_id]:
            return []

        history = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.sessions[session_id])
        return history

    def reset_conversation(self, session_id: Optional[str] = None) -> None:
        """
        Resets the conversation history to the default messages.

        :param session_id: ID of the session (default: None).
        """
        session_id = self._validate_session(session_id)
        self._log(f"Resetting conversation for session `{session_id}`.")

        if len(self.sessions[session_id]) <= 1:  # Only system message exists
            self.logger.warning(f"Session '{session_id}' is already at its default state.")

        self.sessions[session_id] = [self.sessions[session_id][0]] # Preserve system message
        self._save_session_to_disk(session_id)

    def save_conversation(self, file_path: str, session_id: Optional[str] = None) -> None:
        """
        Saves the current conversation history.

        :param file_path: The path to save the conversation history as a JSON file.
        :param session_id: ID of the conversation session (default: None).
        """
        session_id = self._validate_session(session_id)
        self._log(f"Saving conversation for session `{session_id}`.")

        with tempfile.NamedTemporaryFile("w", delete=False) as tmp_file:
            json.dump(self.sessions[session_id], tmp_file)
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(tmp_file.name, file_path)

    def load_conversation(self, file_path: str, session_id: Optional[str] = None) -> None:
        """
        Loads a conversation history from a JSON file.

        :param file_path: The path to the JSON file containing the conversation history.
        :param session_id: ID of the conversation session (default: None).
        """
        session_id = self._validate_session(session_id)
        self._log(f"Loading conversation for session `{session_id}`.")

        try:
            with open(file_path, 'r') as f:
                loaded_session = json.load(f)
                if not isinstance(loaded_session, list):
                    raise ValueError("Invalid conversation format. Expected a list of messages.")

            self.sessions[session_id] = loaded_session
        except FileNotFoundError:
            self.logger.warning(f"File '{file_path}' not found. Starting a fresh session for '{session_id}'.")
            self.reset_conversation(session_id)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in the conversation file.")
        except Exception as e:
            raise e

    async def _request_completion(self, message_content: str, session_id: Optional[str], timeout: int) -> str:
        """
        Internal function to handle synchronous and asynchronous requests to the OpenAI API.

        :param message_content: The user's message.
        :param session_id: ID of the conversation session.
        :param timeout: Request timeout in seconds.
        :return: The LLM's response.
        """
        session_id = self._validate_session(session_id)

        if self.log_messages:
            self._log(f"Requesting completion for session `{session_id}`. Message `{message_content}`")

        new_message = {"role": "user", "content": message_content}
        messages = self.sessions[session_id] + [new_message]

        try:
            completion = await self.async_client.chat.completions.create(
                model=self.llm_model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
                timeout=timeout
            )
            response = completion.choices[0].message.content

            if self.include_message_history:
                self.sessions[session_id].append(new_message)
                self.sessions[session_id].append({"role": "assistant", "content": response})
                self._save_session_to_disk(session_id)

            return response

        # --- Timeout from asyncio or OpenAI directly ---
        except (asyncio.TimeoutError, openai.error.Timeout):
            self.logger.critical(f"The request timed out (timeout={timeout}).", exc_info=True)
            raise

        # --- OpenAI-specific error types ---
        except openai.error.APIError as e:
            self.logger.critical(f"OpenAI API error: {e}", exc_info=True)
            raise
        except openai.error.APIConnectionError as e:
            self.logger.critical(f"Failed to connect to OpenAI API: {e}", exc_info=True)
            raise
        except openai.error.InvalidRequestError as e:
            self.logger.critical(f"Invalid request to OpenAI API: {e}", exc_info=True)
            raise
        except openai.error.AuthenticationError:
            self.logger.critical("Authentication with OpenAI API failed.", exc_info=True)
            raise
        except openai.error.PermissionError:
            self.logger.critical("Permission denied for OpenAI API.", exc_info=True)
            raise
        except openai.error.RateLimitError:
            self.logger.critical("Rate limit exceeded for OpenAI API.", exc_info=True)
            raise

        # --- aiohttp-specific HTTP/connection errors ---
        except aiohttp.ClientResponseError as e:
            self.logger.critical(f"HTTP Error {e.status}: {e.message}", exc_info=True)
            raise OpenAIClientError()
        except aiohttp.ClientConnectionError as e:
            self.logger.critical(f"Connection error while accessing OpenAI API: {e}", exc_info=True)
            raise OpenAIClientError()

        # --- General issues ---
        except ValueError as e:
            self.logger.critical(f"Invalid input: {e}", exc_info=True)
            raise
        except Exception as e:
            self.logger.critical(f"An unexpected error occurred: {e}", exc_info=True)
            raise
        
    def _load_all_sessions_from_disk(self) -> None:
        """
        Loads all session files into memory.
        """
        self.sessions = {}

        for filename in os.listdir(self.SESSION_DIR):
            if filename.endswith(".json"):
                session_id = filename[:-5]  # Remove '.json'

                with open(os.path.join(self.SESSION_DIR, filename), "r") as file:
                    self.sessions[session_id] = json.load(file)

    def _save_session_to_disk(self, session_id: str) -> None:
        """
        Saves a session to a file.

        :param session_id: ID of the conversation session.
        """
        if not self.save_sessions_to_disk or not self.include_message_history:
            return
        
        if not session_id.strip():
            raise ValueError("Session ID cannot be empty.")
        
        filepath = os.path.join(self.SESSION_DIR, f"{session_id}.json")
        with open(filepath, "w") as file:
            json.dump(self.sessions[session_id], file)

    def _validate_session(self, session_id: Optional[str] = None) -> str:
        """
        Validates the session ID and returns a valid session identifier.
        If the session does not exist, initializes it with the default system message.

        :param session_id: The session ID to validate.
        :return: A valid session ID.
        """
        session_id = session_id or "default"
        if session_id not in self.sessions:
            self.sessions[session_id] = [self.default_system_message]
            self._save_session_to_disk(session_id)

        return session_id

    def _validate_initialization_params(self, azure_endpoint: str, api_key: str, api_version: str, llm_model: str) -> None:
        """
        Validates the Azure OpenAI parameters

        :param azure_endpoint: Azure endpoint URL.
        :param api_key: API key for Azure OpenAI.
        :param api_version: API version for Azure OpenAI.
        :param llm_model: The model name to use.
        """
        self._log("Validating Azure OpenAI parameters.")

        if not all([azure_endpoint, api_key, api_version, llm_model]):
            raise OpenAIClientError("Azure OpenAI configuration parameters are missing.")
