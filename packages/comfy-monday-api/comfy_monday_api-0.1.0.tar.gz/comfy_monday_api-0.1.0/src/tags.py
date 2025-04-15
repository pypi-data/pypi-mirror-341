from typing import Dict, Any

from .base import MondayClient


class MondayTags:
    """Class for working with Monday.com tags."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def create_or_get_tag(self, board_id: int, tag_name: str) -> Dict[str, Any]:
        """Get a tag if it exists or create it if it doesn't.

        Note: This functionality might be deprecated in newer Monday.com API versions.

        Args:
            board_id: The ID of the board
            tag_name: The name of the tag to get or create

        Returns:
            Tag data
        """
        # First, try to find the tag
        query = f"""
            query {{
                boards(ids: {board_id}) {{
                    tags {{
                        id
                        name
                        color
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("boards"):
            raise Exception(f"Board with ID {board_id} not found")

        tags = result["data"]["boards"][0]["tags"]

        # Check if the tag already exists
        for tag in tags:
            if tag["name"].lower() == tag_name.lower():
                return tag

        # If not, create a new tag
        query = f"""
            mutation {{
                create_tag(board_id: {board_id}, tag_name: "{tag_name}") {{
                    id
                    name
                    color
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["create_tag"]