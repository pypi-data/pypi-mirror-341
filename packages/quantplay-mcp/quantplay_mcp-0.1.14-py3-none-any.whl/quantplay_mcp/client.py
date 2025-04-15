"""
QuantPlay API client implementation.

This module provides a client for interacting with the QuantPlay API,
handling authentication, request construction, and response parsing.
"""
import json
import logging
from typing import List, Optional, TypeVar, Type

import requests
import aiohttp
from aiohttp import ClientSession, ClientResponse, ClientTimeout

from config import (
    API_ENDPOINT,
    DEFAULT_HEADERS,
    DEFAULT_TIMEOUT,
    ACCOUNTS_ENDPOINT,
    ERROR_INVALID_API_KEY,
    ERROR_API_REQUEST_FAILED,
    ERROR_NETWORK_ERROR,
    ERROR_TIMEOUT,
    ERROR_PARSE_ERROR,
)
from models import Account, APIResponse

# Set up logging
logger = logging.getLogger(__name__)

# Type variables
T = TypeVar('T')
ResponseType = TypeVar('ResponseType', bound=APIResponse)


class QuantPlayAPIError(Exception):
    """Base exception for QuantPlay API errors."""
    pass


class AuthenticationError(QuantPlayAPIError):
    """Raised when authentication fails."""
    pass


class APIRequestError(QuantPlayAPIError):
    """Raised when an API request fails."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(ERROR_API_REQUEST_FAILED.format(
            status_code=status_code, message=message
        ))


class NetworkError(QuantPlayAPIError):
    """Raised when a network error occurs."""
    pass


class TimeoutError(QuantPlayAPIError):
    """Raised when a request times out."""
    pass


class ParseError(QuantPlayAPIError):
    """Raised when response parsing fails."""
    pass


class QuantPlayClient:
    """
    Client for the QuantPlay API.
    
    Provides methods to interact with the QuantPlay API, handling
    authentication, request construction, and response parsing.
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = API_ENDPOINT,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        """
        Initialize the QuantPlay API client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API (default from config)
            timeout: Request timeout in seconds (default from config)
        
        Raises:
            AuthenticationError: If the API key is empty or invalid
        """
        if not api_key:
            raise AuthenticationError(ERROR_INVALID_API_KEY)
        
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        
        # Set up headers with authentication
        self.headers = DEFAULT_HEADERS.copy()
        self.headers["x-api-key"] = api_key
        
        logger.debug(f"Initialized QuantPlay API client with base URL: {base_url}")
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build a full URL for an API endpoint.
        
        Args:
            endpoint: The API endpoint path (e.g., "/accounts")
        
        Returns:
            The full URL for the endpoint
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        
        return f"{self.base_url}{endpoint}"
    
    def _handle_response(
        self, 
        response: requests.Response
    ) -> ResponseType:
        """
        Handle an API response, checking for errors and parsing the response.


        Args:
            response: The requests.Response object
            response_class: The class to parse the response into
        
        Returns:
            Parsed response object
        
        Raises:
            APIRequestError: If the API returns an error
            ParseError: If response parsing fails
        """
        try:
            response.raise_for_status()
            response_data = response.json()
            
            # Check if response has error status
            if (
                isinstance(response_data, dict) and
                response_data.get("error") == True
            ):
                raise APIRequestError(
                    response.status_code,
                    response_data.get("message", "Unknown error")
                )
            return response_data["data"]
        
        except requests.exceptions.HTTPError as e:
            # Try to extract error message from response
            error_message = "Unknown error"
            try:
                error_data = response.json()
                if isinstance(error_data, dict):
                    error_message = error_data.get("message", "Unknown error")
            except:
                error_message = response.text or "Unknown error"
            
            raise APIRequestError(response.status_code, error_message) from e
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {e}")
            raise ParseError(ERROR_PARSE_ERROR.format(error=str(e))) from e
    
    async def _handle_async_response(
        self, 
        response: ClientResponse, 
        response_class: Type[ResponseType]
    ) -> ResponseType:
        """
        Handle an async API response, checking for errors and parsing the response.
        
        Args:
            response: The aiohttp ClientResponse object
            response_class: The class to parse the response into
        
        Returns:
            Parsed response object
        
        Raises:
            APIRequestError: If the API returns an error
            ParseError: If response parsing fails
        """
        try:
            if not response.ok:
                error_message = "Unknown error"
                try:
                    error_data = await response.json()
                    if isinstance(error_data, dict):
                        error_message = error_data.get("message", "Unknown error")
                except:
                    error_message = await response.text() or "Unknown error"
                
                raise APIRequestError(response.status, error_message)
            
            response_data = await response.json()
            
            # Check if response has error status
            if (
                isinstance(response_data, dict) and
                response_data.get("status") == "error"
            ):
                raise APIRequestError(
                    response.status,
                    response_data.get("message", "Unknown error")
                )
            
            return response_class.from_dict(response_data)
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {e}")
            raise ParseError(ERROR_PARSE_ERROR.format(error=str(e))) from e
    
    def get_accounts(self) -> List[Account]:
        """
        Get all accounts from the API.
        
        Returns:
            List of Account objects
        
        Raises:
            APIRequestError: If the API returns an error
            NetworkError: If a network error occurs
            TimeoutError: If the request times out
            ParseError: If response parsing fails
        """
        url = self._build_url(ACCOUNTS_ENDPOINT)
        
        try:

            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
            )

            accounts_response = self._handle_response(response)
            return accounts_response
        
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {e}")
            raise TimeoutError(ERROR_TIMEOUT.format(timeout=self.timeout)) from e
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network error: {e}")
            raise NetworkError(ERROR_NETWORK_ERROR.format(error=str(e))) from e
        
        except (requests.exceptions.RequestException, QuantPlayAPIError) as e:
            if not isinstance(e, QuantPlayAPIError):
                logger.error(f"Request failed: {e}")
                raise NetworkError(ERROR_NETWORK_ERROR.format(error=str(e))) from e
            raise
    
    async def async_get_accounts(self, session: Optional[ClientSession] = None) -> List[Account]:
        """
        Get all accounts from the API asynchronously.
        
        Args:
            session: Optional existing aiohttp ClientSession
        
        Returns:
            List of Account objects
        
        Raises:
            APIRequestError: If the API returns an error
            NetworkError: If a network error occurs
            TimeoutError: If the request times out
            ParseError: If response parsing fails
        """
        url = self._build_url(ACCOUNTS_ENDPOINT)
        client_timeout = ClientTimeout(total=self.timeout)
        
        # Create a new session if one wasn't provided
        should_close_session = session is None
        if session is None:
            session = aiohttp.ClientSession(timeout=client_timeout)
        
        try:
            async with session.get(url, headers=self.headers) as response:
                accounts_response = await self._handle_async_response(response, AccountsResponse)
                return accounts_response.data
        
        except asyncio.TimeoutError as e:
            logger.error(f"Async request timed out: {e}")
            raise TimeoutError(ERROR_TIMEOUT.format(timeout=self.timeout)) from e
        
        except aiohttp.ClientConnectorError as e:
            logger.error(f"Async network error: {e}")
            raise NetworkError(ERROR_NETWORK_ERROR.format(error=str(e))) from e
        
        except (aiohttp.ClientError, QuantPlayAPIError) as e:
            if not isinstance(e, QuantPlayAPIError):
                logger.error(f"Async request failed: {e}")
                raise NetworkError(ERROR_NETWORK_ERROR.format(error=str(e))) from e
            raise
        
        finally:
            # Close the session if we created it
            if should_close_session and session is not None:
                await session.close()


# For backward compatibility and convenience
Client = QuantPlayClient

