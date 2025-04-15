from typing import Dict, List, Any

from .base import MondayClient


class MondayTeams:
    """Class for working with Monday.com teams."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def list_teams(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieves a list of teams.

        Args:
            limit: Maximum number of teams to return (default: 100)

        Returns:
            List of team data
        """
        query = f"""
            query {{
                teams(limit: {limit}) {{
                    id
                    name
                    picture_url
                    users {{
                        id
                        name
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["teams"]

    def list_team_members(self, team_id: int) -> List[Dict[str, Any]]:
        """Retrieves a list of members by team ID.

        Args:
            team_id: The ID of the team

        Returns:
            List of team member data
        """
        query = f"""
            query {{
                teams(ids: {team_id}) {{
                    users {{
                        id
                        name
                        email
                        photo_thumb
                        title
                        position
                        location
                        status
                        phone
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("teams"):
            raise Exception(f"Team with ID {team_id} not found")

        return result["data"]["teams"][0]["users"]

    def get_team(self, team_id: int) -> Dict[str, Any]:
        """Returns a team by ID.

        Args:
            team_id: The ID of the team

        Returns:
            Team data
        """
        query = f"""
            query {{
                teams(ids: {team_id}) {{
                    id
                    name
                    picture_url
                    users {{
                        id
                        name
                        email
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("teams"):
            raise Exception(f"Team with ID {team_id} not found")

        return result["data"]["teams"][0]