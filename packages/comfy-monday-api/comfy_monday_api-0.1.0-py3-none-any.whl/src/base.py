import requests

from typing import Dict, Any


class MondayClient:
    """Basic client for interacting with the Monday.com GraphQL API."""

    def __init__(self, token: str, api_url: str = "https://api.monday.com/v2"):
        """Initialize the Monday client.

        Args:
            token: The API token for authentication
            api_url: The Monday.com API URL (default: "https://api.monday.com/v2")
        """
        self.token = token
        self.api_url = api_url
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        self._query = ""  # Initialize an empty query

    def _exec_query(self) -> Dict[str, Any]:
        """Execute the stored GraphQL query against the Monday.com API.

        This method uses the stored _query instance variable.

        Returns:
            The response from the API as a dictionary

        Raises:
            Exception: If the API request fails or if no query is set
        """
        if not self._query:
            raise Exception("No query set. Set the _query property before calling _exec_query.")

        data = {"query": self._query}

        response = requests.post(
            self.api_url,
            json=data,
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(
                f"API request failed with status code {response.status_code}: {response.text}"
            )

        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL query failed: {result['errors']}")

        return result


def execute_graph_query(client: MondayClient, query: str) -> Dict[str, Any]:
    """Executes a custom GraphQL query using the Monday.com API.

    Args:
        client: An initialized MondayClient instance
        query: The GraphQL query to execute

    Returns:
        The response from the API as a dictionary
    """
    client._query = query
    return client._exec_query()