import pickle
import logging
from pathlib import Path

from ..utility_base import UtilityBase
from ..logger import Logger, LogWrapper

from typing import Optional
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError, ClientAuthenticationError, ServiceRequestError
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import ContentFormat, AnalyzeResult


# Unified custom exception
class DocumentIntelligenceClientError(Exception):
    pass


class AzureDocumentIntelligenceClient(UtilityBase):
    """
    A wrapper for interacting with Azure Document Intelligence API.
    """

    def __init__(
            self, 
            endpoint: str, 
            api_key: str,
            verbose: bool = False,
            logger: Optional[logging.Logger | Logger | LogWrapper] = None,
            log_level: Optional[int] = None
        ):
        """
        Initializes the AzureDocumentIntelligenceClient.

        :param endpoint: Azure Document Intelligence endpoint.
        :param api_key: API key for Azure Document Intelligence.
        :param log_messages: If true messages and system messages are logged too.
        :param logger: Optional logger instance. If not provided, a default logger is used.
        :param log_level: Optional log level. If not provided INFO level will be used for logging
        """
        # Init base class
        super().__init__(verbose, logger, log_level)

        if not endpoint or not api_key:
            raise DocumentIntelligenceClientError("Both endpoint and API key are required.")

        self.endpoint = endpoint
        self.api_key = api_key

        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
            headers={"x-ms-useragent": "document-intelligence-wrapper/1.0.0"}
        )

    def _get_cache_path(self, file_path: Path) -> Path:
        """
        Generate the path to the cached pickle file.
        """
        return file_path.parent / f"docint_{file_path.stem}.pkl"

    def parse_document(self, file_path: str, output_format: ContentFormat = ContentFormat.MARKDOWN) -> str:
        """
        Parses a document and returns the result content. Caches the result locally in a .pkl file.

        :param file_path: Path to the document file.
        :param output_format: Desired content format.
        :return: Parsed document content.
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        cache_path = self._get_cache_path(file_path)

        if cache_path.exists():
            raise DocumentIntelligenceClientError(f"Cached result already exists: {cache_path}. Delete the file to reprocess.")

        try:
            if self.verbose:
                self.logger.log(self.log_level, f"Parsing document `{file_path}`...")

            with file_path.open("rb") as file:
                poller = self.client.begin_analyze_document(
                    model_id="prebuilt-layout",
                    analyze_request=file,
                    content_type="application/octet-stream",
                    output_content_format=output_format
                )
                result: AnalyzeResult = poller.result()

            with cache_path.open("wb") as f:
                pickle.dump(result, f)

            if self.verbose:
                self.logger.log(self.log_level, f"Parsing done, saving result to `{cache_path}`")

            return result.content

        except ClientAuthenticationError as e:
            self.logger.critical(f"Client authentication error while parsing `{file_path.name}`: {e}", exc_info=True)
            raise
        except HttpResponseError as e:
            self.logger.critical(f"HTTP error occurred: `{e.message}` while parsing `{file_path.name}`", exc_info=True)
            raise
        except ServiceRequestError as e:
            self.logger.critical(f"Network or service request failure while parsing `{file_path.name}`: {e}", exc_info=True)
            raise 
        except Exception as e:
            self.logger.critical(f"Unexpected error during document parsing `{file_path.name}`: {e}", exc_info=True)
            raise
