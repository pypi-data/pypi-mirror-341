from typing import Dict, List, Any, Optional

from .base import MondayClient


class MondayUpdates:
    """Class for working with Monday.com updates."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def list_updates(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get a list of all updates.

        Args:
            limit: Maximum number of updates to return (default: 100)

        Returns:
            List of update data
        """
        query = f"""
            query {{
                updates(limit: {limit}) {{
                    id
                    body
                    created_at
                    updated_at
                    creator {{
                        id
                        name
                    }}
                    item_id
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["updates"]

    def list_item_updates(self, item_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Get a list of updates for a specific item.

        Args:
            item_id: The ID of the item
            limit: Maximum number of updates to return (default: 100)

        Returns:
            List of update data for the specified item
        """
        query = f"""
            query {{
                items(ids: {item_id}) {{
                    updates(limit: {limit}) {{
                        id
                        body
                        created_at
                        updated_at
                        creator {{
                            id
                            name
                        }}
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("items"):
            raise Exception(f"Item with ID {item_id} not found")

        return result["data"]["items"][0]["updates"]

    def create_update(
            self,
            item_id: int,
            body: str,
            parent_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create a new update for an item.

        Args:
            item_id: The ID of the item to update
            body: The text content of the update
            parent_id: Optional ID of a parent update (for replies)

        Returns:
            Data of the created update
        """
        parent_param = f', parent_id: {parent_id}' if parent_id else ''

        query = f"""
            mutation {{
                create_update(item_id: {item_id}, body: "{body}"{parent_param}) {{
                    id
                    body
                    created_at
                    creator_id
                    item_id
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["create_update"]