"""
Main client class for interacting with the Enemera API.
"""

import requests
from typing import Dict, Any, Optional, List, Union

from enemera.constants import BASE_URL, DEFAULT_TIMEOUT
from enemera.exceptions import AuthenticationError, APIError, ConnectionError, RateLimitError
from enemera.namespace import ItalyNamespace


class EnemeraClient:
    """
    Client for interacting with the Enemera API.
    """

    def __init__(
            self,
            api_key: str,
            base_url: str = BASE_URL,
            timeout: int = DEFAULT_TIMEOUT
    ):
        """
        Initialize the Enemera API client.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API (defaults to the production API)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

        # Set up authentication header
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

        # Initialize namespaces
        self.italy = ItalyNamespace(self)

        # Provide direct access to prices API for backward compatibility
        self.prices = self.italy.prices

    def request(
            self,
            method: str,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            data: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a request to the Enemera API.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data

        Returns:
            Response data as a dictionary or list of dictionaries

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            APIError: If the API returns an error
            ConnectionError: If connection to the API fails
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout
            )

            # Handle different HTTP status codes
            if response.status_code == 200:
                return response.json() if response.content else {}
            elif response.status_code == 401:
                raise AuthenticationError("Authentication failed. Check your API key.")
            elif response.status_code == 429:
                raise RateLimitError("API rate limit exceeded. Please slow down your requests.")
            else:
                # Try to get error details from response
                try:
                    error_data = response.json()
                    detail = error_data.get('message', 'Unknown error')
                except:
                    detail = response.text or 'Unknown error'

                raise APIError(response.status_code, detail)

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Connection to API failed: {str(e)}")
            #APIError(response.status_code, detail)

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Connection to API failed: {str(e)}")