import json

from typing import Dict, List, Any, Optional, Union

from .base import MondayClient


class MondayBoards:
    """Class for working with Monday.com boards, groups, items and columns."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def get_item_column_value(self, item_id: int, column_id: str) -> Dict[str, Any]:
        """Get a specific column value from an item (pulse).

        Args:
            item_id: The ID of the item
            column_id: The ID of the column

        Returns:
            The value of the specified column
        """
        query = f"""
            query {{
                items(ids: {item_id}) {{
                    column_values(ids: ["{column_id}"]) {{
                        id
                        text
                        value
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("items"):
            raise Exception(f"Item with ID {item_id} not found")

        column_values = result["data"]["items"][0]["column_values"]
        if not column_values:
            raise Exception(f"Column with ID {column_id} not found on item {item_id}")

        return column_values[0]

    def update_item_column_values(self, item_id: int, board_id: int, column_values: Dict[str, Any]) -> Dict[str, Any]:
        """Update one or more column values of a specific item.

        Args:
            item_id: The ID of the item to update
            board_id: The ID of the board containing the item
            column_values: Dictionary mapping column IDs to their new values

        Returns:
            Updated item data
        """
        column_values_json = json.dumps(column_values)

        query = f"""
            mutation {{
                change_multiple_column_values(item_id: {item_id}, board_id: {board_id}, column_values: {column_values_json}) {{
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

        return result["data"]["change_multiple_column_values"]

    def list_boards(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List all accessible boards.

        Args:
            limit: Maximum number of boards to return (default: 100)

        Returns:
            List of board data
        """
        query = f"""
            query {{
                boards(limit: {limit}) {{
                    id
                    name
                    description
                    board_kind
                    state
                    owner {{
                        id
                        name
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["boards"]

    def list_board_groups(self, board_id: int) -> List[Dict[str, Any]]:
        """List all groups in a specific board.

        Args:
            board_id: The ID of the board

        Returns:
            List of group data
        """
        query = f"""
            query {{
                boards(ids: {board_id}) {{
                    groups {{
                        id
                        title
                        color
                        position
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("boards"):
            raise Exception(f"Board with ID {board_id} not found")

        return result["data"]["boards"][0]["groups"]

    def add_column_to_board(
            self,
            board_id: int,
            title: str,
            column_type: str,
            defaults: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add a new column to a board.

        Args:
            board_id: The ID of the board
            title: The title of the new column
            column_type: The type of the column (e.g., "text", "number", "date")
            defaults: Optional default values for the column

        Returns:
            Data of the created column
        """
        defaults_json = json.dumps(defaults) if defaults else "{}"

        query = f"""
            mutation {{
                create_column(board_id: {board_id}, title: "{title}", column_type: {column_type}, defaults: {defaults_json}) {{
                    id
                    title
                    type
                    settings_str
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["create_column"]

    def create_board(
            self,
            board_name: str,
            board_kind: str = "public",
            description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new board.

        Args:
            board_name: The name of the new board
            board_kind: The kind of board (default: "public")
            description: Optional description for the board

        Returns:
            Data of the created board
        """
        description_param = f'"{description}"' if description else "null"

        query = f"""
            mutation {{
                create_board(board_name: "{board_name}", board_kind: {board_kind}, description: {description_param}) {{
                    id
                    name
                    description
                    board_kind
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["create_board"]

    def get_board(self, board_id: int) -> Dict[str, Any]:
        """Get data about a specific board.

        Args:
            board_id: The ID of the board

        Returns:
            Board data
        """
        query = f"""
            query {{
                boards(ids: {board_id}) {{
                    id
                    name
                    description
                    state
                    board_kind
                    columns {{
                        id
                        title
                        type
                    }}
                    groups {{
                        id
                        title
                    }}
                    owner {{
                        id
                        name
                    }}
                    permissions
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("boards"):
            raise Exception(f"Board with ID {board_id} not found")

        return result["data"]["boards"][0]

    def get_group(self, board_id: int, group_id: str) -> Dict[str, Any]:
        """Get data about a specific group.

        Args:
            board_id: The ID of the board containing the group
            group_id: The ID of the group

        Returns:
            Group data
        """
        query = f"""
            query {{
                boards(ids: {board_id}) {{
                    groups(ids: ["{group_id}"]) {{
                        id
                        title
                        color
                        position
                        items {{
                            id
                            name
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

        return groups[0]

    def duplicate_board(
            self,
            board_id: int,
            board_name: Optional[str] = None,
            duplicate_type: str = "duplicate_board_with_structure"
    ) -> Dict[str, Any]:
        """Duplicate a board.

        Args:
            board_id: The ID of the board to duplicate
            board_name: Optional name for the new board (default: same as original with "copy" suffix)
            duplicate_type: Type of duplication (default: "duplicate_board_with_structure")

        Returns:
            Data of the duplicated board
        """
        board_name_param = f'"{board_name}"' if board_name else "null"

        query = f"""
            mutation {{
                duplicate_board(board_id: {board_id}, duplicate_type: {duplicate_type}, board_name: {board_name_param}) {{
                    board {{
                        id
                        name
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["duplicate_board"]["board"]

    def duplicate_group(
            self,
            board_id: int,
            group_id: str,
            group_title: Optional[str] = None,
            add_to_top: bool = False
    ) -> Dict[str, Any]:
        """Duplicate a group.

        Args:
            board_id: The ID of the board containing the group
            group_id: The ID of the group to duplicate
            group_title: Optional title for the new group (default: same as original with "copy" suffix)
            add_to_top: If True, adds the duplicated group to the top of the board (default: False)

        Returns:
            Data of the duplicated group
        """
        group_title_param = f'"{group_title}"' if group_title else "null"

        query = f"""
            mutation {{
                duplicate_group(board_id: {board_id}, group_id: "{group_id}", group_title: {group_title_param}, add_to_top: {str(add_to_top).lower()}) {{
                    group {{
                        id
                        title
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["duplicate_group"]["group"]