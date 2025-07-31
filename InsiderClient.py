import requests
import json
from typing import Dict, Any, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InsiderAPIClient:
    """
    A Python client for interacting with Insider REST API
    """

    def __init__(self, base_url: str, api_key: str = None, timeout: int = 30):
        """
        Initialize the API client

        Args:
            base_url: Base URL of the API (e.g., 'https://api.insider.com')
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

        # Add API key to headers if provided
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}',
                # Alternative auth header formats:
                # 'X-API-Key': self.api_key,
                # 'Authorization': f'API-Key {self.api_key}'
            })

    def _make_request(self, method: str, endpoint: str, headers: Optional[Dict[str, Any]] = None,
                      data: Optional[Dict[str, Any]] = None,
                      params: Optional[Dict[str, Any]] = None,) -> requests.Response:
        """
        Make HTTP request to the API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            data: JSON data for request body
            params: URL parameters

        Returns:
            requests.Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            # Log the request
            logger.info(f"{method.upper()} {url} - Status: {response.status_code}")

            # Raise exception for bad status codes
            response.raise_for_status()

            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send GET request

        Args:
            endpoint: API endpoint
            params: URL parameters

        Returns:
            JSON response as dictionary
        """
        response = self._make_request('GET', endpoint, params=params)
        return response.json()

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send POST request

        Args:
            endpoint: API endpoint
            data: JSON data for request body

        Returns:
            JSON response as dictionary
        """
        response = self._make_request('POST', endpoint, data=data)
        return response.json()

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send PUT request

        Args:
            endpoint: API endpoint
            data: JSON data for request body

        Returns:
            JSON response as dictionary
        """
        response = self._make_request('PUT', endpoint, data=data)
        return response.json()

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Send DELETE request

        Args:
            endpoint: API endpoint

        Returns:
            JSON response as dictionary
        """
        response = self._make_request('DELETE', endpoint)
        return response.json()

# Example usage
def main():
    """
    Example of how to use the InsiderAPIClient
    """

    # Initialize the client
    # Replace with actual Insider API URL and your API key
    client = InsiderAPIClient(
        base_url='https://contact.useinsider.com/email/v1',  # Replace with actual URL
        api_key='887afbc3b32e97014ec0c2095b206f94aa3698261ce4922b75c02655670e99'  # Replace with your actual API key
    )

    try:
        # Example 1: GET request to fetch user data
        # print("Fetching user data...")
        # users = client.get('users', params={'limit': 10})
        # print(f"Retrieved {len(users.get('data', []))} users")

        # Example 2: POST request to create a new resource

        url = "https://contact.useinsider.com/email/v1/unsubscribe"

        payload = json.dumps({
            "email": "sample@useinsider.com"
        })


        response = requests.request("POST", url, headers, data=payload)

        print(response.text)




        print("\nCreating new resource...")

        headers = {
            'X-PARTNER-NAME': '',
            'X-REQUEST-TOKEN': '',
            'Content-Type': 'application/json'
        }


        payload = {
            'name': 'Updated Test User',
            'email': 'updated@example.com'
        }

        created_user = client.post('unsubscribe', headers=headers, data=payload)
        print(f"Created user with ID: {created_user.get('id')}")

        # # Example 3: PUT request to update a resource
        # print("\nUpdating resource...")
        # update_data = {
        #     'name': 'Updated Test User',
        #     'email': 'updated@example.com'
        # }
        # updated_user = client.put('users/123', data=update_data)
        # print(f"Updated user: {updated_user.get('name')}")
        #
        # # Example 4: DELETE request
        # print("\nDeleting resource...")
        # result = client.delete('users/123')
        # print(f"Delete result: {result}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Alternative simple function-based approach
def send_insider_request(method: str, endpoint: str,
                         data: Optional[Dict] = None,
                         api_key: Optional[str] = None) -> Dict:
    """
    Simple function to send requests to Insider API

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: Full API endpoint URL
        data: Data to send in request body
        api_key: API key for authentication

    Returns:
        JSON response as dictionary
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    try:
        response = requests.request(
            method=method.upper(),
            url=endpoint,
            json=data,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        raise


if __name__ == "__main__":
    main()