from typing import Dict, List, Any, Optional

from .base import MondayClient


class MondayActivities:
    """Class for working with Monday.com activity logs."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def list_board_activity_logs(
            self,
            board_id: int,
            limit: int = 100,
            page: int = 1,
            from_date: Optional[str] = None,
            to_date: Optional[str] = None,
            user_ids: Optional[List[int]] = None,
            column_ids: Optional[List[str]] = None,
            group_ids: Optional[List[str]] = None,
            item_ids: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves a list of board activity logs.

        Args:
            board_id: The ID of the board
            limit: Maximum number of activities to return (default: 100)
            page: Page number for pagination (default: 1)
            from_date: Optional start date for filtering (ISO format: "YYYY-MM-DD")
            to_date: Optional end date for filtering (ISO format: "YYYY-MM-DD")
            user_ids: Optional list of user IDs to filter by
            column_ids: Optional list of column IDs to filter by
            group_ids: Optional list of group IDs to filter by
            item_ids: Optional list of item IDs to filter by

        Returns:
            List of activity log data
        """
        # Build filter parameters
        filter_params = []

        if from_date:
            filter_params.append(f'from: "{from_date}"')

        if to_date:
            filter_params.append(f'to: "{to_date}"')

        if user_ids:
            user_ids_str = str(user_ids).replace("'", "")
            filter_params.append(f'user_ids: {user_ids_str}')

        if column_ids:
            column_ids_str = str(column_ids).replace("'", '"')
            filter_params.append(f'column_ids: {column_ids_str}')

        if group_ids:
            group_ids_str = str(group_ids).replace("'", '"')
            filter_params.append(f'group_ids: {group_ids_str}')

        if item_ids:
            item_ids_str = str(item_ids).replace("'", "")
            filter_params.append(f'item_ids: {item_ids_str}')

        filter_str = ", ".join(filter_params)
        if filter_str:
            filter_str = f", {filter_str}"

        query = f"""
            query {{
                boards(ids: {board_id}) {{
                    activity_logs(limit: {limit}, page: {page}{filter_str}) {{
                        id
                        entity
                        event
                        created_at
                        data
                        user {{
                            id
                            name
                            email
                        }}
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("boards"):
            raise Exception(f"Board with ID {board_id} not found")

        return result["data"]["boards"][0]["activity_logs"]