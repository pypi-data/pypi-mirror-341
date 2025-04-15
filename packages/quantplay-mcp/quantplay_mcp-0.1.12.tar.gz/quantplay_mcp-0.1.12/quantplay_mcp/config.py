"""
Configuration module for QuantPlay API client.
Contains constants and settings used throughout the client.
"""
from typing import Dict, Any, Optional

# API Base URL
API_BASE_URL: str = "https://dms.quantplay.tech"
API_VERSION: str = "v2"
API_ENDPOINT: str = f"{API_BASE_URL}/{API_VERSION}"

# Request configuration
DEFAULT_TIMEOUT: int = 30  # seconds
DEFAULT_HEADERS: Dict[str, str] = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Endpoints
ACCOUNTS_ENDPOINT: str = "/accounts"

# Error messages
ERROR_INVALID_API_KEY: str = "Invalid API key provided"
ERROR_API_REQUEST_FAILED: str = "API request failed: {status_code} - {message}"
ERROR_NETWORK_ERROR: str = "Network error occurred while connecting to QuantPlay API: {error}"
ERROR_TIMEOUT: str = "Request to QuantPlay API timed out after {timeout} seconds"
ERROR_PARSE_ERROR: str = "Failed to parse API response: {error}"

