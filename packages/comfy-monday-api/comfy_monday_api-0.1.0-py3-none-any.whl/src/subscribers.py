from typing import Dict, List, Any

from .base import MondayClient


class MondaySubscribers:
    """Class for working with Monday.com subscribers."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def list_item_subscribers(self, item_id: int) -> List[Dict[str, Any]]:
        """Retrieves a list of item's (pulse's) subscribers.

        Args:
            item_id: The ID of the item

        Returns:
            List of subscriber data
        """
        query = f"""
            query {{
                items(ids: {item_id}) {{
                    subscribers {{
                        id
                        name
                        email
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("items"):
            raise Exception(f"Item with ID {item_id} not found")

        return result["data"]["items"][0]["subscribers"]

    def list_board_subscribers(self, board_id: int) -> List[Dict[str, Any]]:
        """Retrieves a list of subscribers of a board by the board ID.

        Args:
            board_id: The ID of the board

        Returns:
            List of subscriber data
        """
        query = f"""
            query {{
                boards(ids: {board_id}) {{
                    subscribers {{
                        id
                        name
                        email
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("boards"):
            raise Exception(f"Board with ID {board_id} not found")

        return result["data"]["boards"][0]["subscribers"]

    def add_board_subscribers(
            self,
            board_id: int,
            user_ids: List[int]
    ) -> Dict[str, Any]:
        """Adds subscribers to a board by their IDs and the board ID.

        Args:
            board_id: The ID of the board
            user_ids: List of user IDs to add as subscribers

        Returns:
            Data of the updated board with subscribers
        """
        # Convert list of IDs to string format for GraphQL
        user_ids_str = str(user_ids).replace("'", "")

        query = f"""
            mutation {{
                add_subscribers_to_board(board_id: {board_id}, user_ids: {user_ids_str}) {{
                    id
                    name
                    subscribers {{
                        id
                        name
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["add_subscribers_to_board"]

    def remove_board_subscribers(
            self,
            board_id: int,
            user_ids: List[int]
    ) -> Dict[str, Any]:
        """Removes subscribers from a board by their IDs and the board ID.

        Args:
            board_id: The ID of the board
            user_ids: List of user IDs to remove as subscribers

        Returns:
            Data of the updated board without subscribers
        """
        # Convert list of IDs to string format for GraphQL
        user_ids_str = str(user_ids).replace("'", "")

        query = f"""
            mutation {{
                remove_subscribers_from_board(board_id: {board_id}, user_ids: {user_ids_str}) {{
                    id
                    name
                    subscribers {{
                        id
                        name
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["remove_subscribers_from_board"]