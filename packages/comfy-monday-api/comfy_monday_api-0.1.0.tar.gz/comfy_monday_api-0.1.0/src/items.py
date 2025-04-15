import json

from typing import Dict, List, Any, Optional

from .base import MondayClient


class MondayItems:
    """Class for working with Monday.com items (pulses)."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def list_board_items(
            self,
            board_id: int,
            limit: int = 100,
            page: int = 1
    ) -> List[Dict[str, Any]]:
        """Get a list of all items on a board.

        Args:
            board_id: The ID of the board
            limit: Maximum number of items to return (default: 100)
            page: Page number for pagination (default: 1)

        Returns:
            List of item data
        """
        query = f"""
            query {{
                boards(ids: {board_id}) {{
                    items(limit: {limit}, page: {page}) {{
                        id
                        name
                        created_at
                        updated_at
                        column_values {{
                            id
                            text
                            value
                        }}
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("boards"):
            raise Exception(f"Board with ID {board_id} not found")

        return result["data"]["boards"][0]["items"]

    def list_group_items(
            self,
            board_id: int,
            group_id: str,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get a list of all items in a group.

        Args:
            board_id: The ID of the board
            group_id: The ID of the group
            limit: Maximum number of items to return (default: 100)

        Returns:
            List of item data
        """
        query = f"""
            query {{
                boards(ids: {board_id}) {{
                    groups(ids: ["{group_id}"]) {{
                        items(limit: {limit}) {{
                            id
                            name
                            created_at
                            updated_at
                            column_values {{
                                id
                                text
                                value
                            }}
                        }}
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("boards"):
            raise Exception(f"Board with ID {board_id} not found")

        groups = result["data"]["boards"][0]["groups"]
        if not groups:
            raise Exception(f"Group with ID {group_id} not found in board {board_id}")

        return groups[0]["items"]

    def search_items_by_column_value(
            self,
            board_id: int,
            column_id: str,
            value: str,
            limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Search for items by column value.

        Args:
            board_id: The ID of the board
            column_id: The ID of the column to search in
            value: The value to search for
            limit: Maximum number of items to return (default: 100)

        Returns:
            List of matching item data
        """
        query = f"""
            query {{
                items_by_column_values(board_id: {board_id}, column_id: "{column_id}", column_value: "{value}", limit: {limit}) {{
                    id
                    name
                    created_at
                    updated_at
                    group {{
                        id
                        title
                    }}
                    column_values {{
                        id
                        text
                        value
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["items_by_column_values"]

    def create_item(
            self,
            board_id: int,
            group_id: str,
            item_name: str,
            column_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new item.

        Args:
            board_id: The ID of the board
            group_id: The ID of the group
            item_name: The name of the new item
            column_values: Optional dictionary of column values

        Returns:
            Data of the created item
        """
        column_values_json = json.dumps(column_values) if column_values else "{}"

        query = f"""
            mutation {{
                create_item(board_id: {board_id}, group_id: "{group_id}", item_name: "{item_name}", column_values: {column_values_json}) {{
                    id
                    name
                    group {{
                        id
                        title
                    }}
                    column_values {{
                        id
                        text
                        value
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["create_item"]

    def create_subitem(
            self,
            parent_item_id: int,
            item_name: str,
            column_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new subitem.

        Args:
            parent_item_id: The ID of the parent item
            item_name: The name of the new subitem
            column_values: Optional dictionary of column values

        Returns:
            Data of the created subitem
        """
        column_values_json = json.dumps(column_values) if column_values else "{}"

        query = f"""
            mutation {{
                create_subitem(parent_item_id: {parent_item_id}, item_name: "{item_name}", column_values: {column_values_json}) {{
                    id
                    name
                    column_values {{
                        id
                        text
                        value
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["create_subitem"]

    def get_item(self, item_id: int) -> Dict[str, Any]:
        """Get data about a specific item.

        Args:
            item_id: The ID of the item

        Returns:
            Item data
        """
        query = f"""
            query {{
                items(ids: {item_id}) {{
                    id
                    name
                    created_at
                    updated_at
                    board {{
                        id
                        name
                    }}
                    group {{
                        id
                        title
                    }}
                    column_values {{
                        id
                        title
                        text
                        value
                        type
                    }}
                    subitems {{
                        id
                        name
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("items"):
            raise Exception(f"Item with ID {item_id} not found")

        return result["data"]["items"][0]

    def move_item_to_group(
            self,
            item_id: int,
            group_id: str
    ) -> Dict[str, Any]:
        """Move an item to a different group.

        Args:
            item_id: The ID of the item to move
            group_id: The ID of the destination group

        Returns:
            Data of the moved item
        """
        query = f"""
            mutation {{
                move_item_to_group(item_id: {item_id}, group_id: "{group_id}") {{
                    id
                    name
                    group {{
                        id
                        title
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["move_item_to_group"]

    def duplicate_item(
            self,
            board_id: int,
            item_id: int,
            with_updates: bool = True
    ) -> Dict[str, Any]:
        """Create a duplicate of an item.

        Args:
            board_id: The ID of the board containing the item
            item_id: The ID of the item to duplicate
            with_updates: Whether to copy updates from the original item (default: True)

        Returns:
            Data of the duplicated item
        """
        query = f"""
            mutation {{
                duplicate_item(board_id: {board_id}, item_id: {item_id}, with_updates: {str(with_updates).lower()}) {{
                    id
                    name
                    board {{
                        id
                    }}
                    group {{
                        id
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["duplicate_item"]

    def delete_item(self, item_id: int) -> Dict[str, Any]:
        """Delete an item permanently.

        Args:
            item_id: The ID of the item to delete

        Returns:
            Status of the deletion
        """
        query = f"""
            mutation {{
                delete_item(item_id: {item_id}) {{
                    id
                    deleted
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["delete_item"]

    def archive_item(self, item_id: int) -> Dict[str, Any]:
        """Archive an item.

        Args:
            item_id: The ID of the item to archive

        Returns:
            Status of the archiving
        """
        query = f"""
            mutation {{
                archive_item(item_id: {item_id}) {{
                    id
                    state
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["archive_item"]