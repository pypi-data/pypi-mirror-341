from typing import Dict, List, Any, Optional

from .base import MondayClient


class MondayUsers:
    """Class for working with Monday.com users."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def list_users(self, kind: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get a list of users.

        Args:
            kind: Optional filter for user kinds (e.g., "all", "non_guests", "guests", etc.)
            limit: Maximum number of users to return (default: 100)

        Returns:
            List of user data
        """
        kind_param = f'kind: {kind}' if kind else ''

        query = f"""
            query {{
                users({kind_param}, limit: {limit}) {{
                    id
                    name
                    email
                    url
                    photo_thumb
                    title
                    location
                    status
                    phone
                    birthday
                    is_guest
                    created_at
                    enabled
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["users"]

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get data about a specific user.

        Args:
            user_id: The ID of the user

        Returns:
            User data
        """
        query = f"""
            query {{
                users(ids: {user_id}) {{
                    id
                    name
                    email
                    url
                    photo_thumb
                    title
                    location
                    status
                    phone
                    birthday
                    is_guest
                    created_at
                    teams {{
                        id
                        name
                    }}
                    account {{
                        id
                        name
                        tier
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("users"):
            raise Exception(f"User with ID {user_id} not found")

        return result["data"]["users"][0]