from typing import Dict, List, Any, Optional, BinaryIO
import base64
import requests
from .base import MondayClient


class MondayFiles:
    """Class for working with Monday.com files and assets."""

    def __init__(self, client: MondayClient):
        """Initialize with a MondayClient instance.

        Args:
            client: An initialized MondayClient instance
        """
        self.client = client

    def list_files(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Returns a list of files based on collection of assets.

        Args:
            limit: Maximum number of files to return (default: 100)

        Returns:
            List of file data
        """
        query = f"""
            query {{
                assets(limit: {limit}) {{
                    id
                    name
                    url
                    file_size
                    file_extension
                    created_at
                    uploaded_by {{
                        id
                        name
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["assets"]

    def add_file_to_update(
            self,
            update_id: int,
            file_path: str
    ) -> Dict[str, Any]:
        """Adds a file to an existing update.

        Args:
            update_id: The ID of the update
            file_path: Path to the file to upload

        Returns:
            Data of the uploaded file and the updated update
        """
        # First, read the file and encode it
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # Get the file name from the path
        file_name = file_path.split('/')[-1]

        # Encode file to base64
        base64_content = base64.b64encode(file_content).decode('utf-8')

        query = f"""
            mutation {{
                add_file_to_update(update_id: {update_id}, file: "{file_name}", content: "{base64_content}") {{
                    id
                    file_extension
                    file_size
                    name
                    url
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["add_file_to_update"]

    def add_file_to_column(
            self,
            item_id: int,
            column_id: str,
            file_path: str
    ) -> Dict[str, Any]:
        """Adds a file to a file column value.

        Args:
            item_id: The ID of the item
            column_id: The ID of the file column
            file_path: Path to the file to upload

        Returns:
            Data of the uploaded file and the updated column
        """
        # First, read the file and encode it
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # Get the file name from the path
        file_name = file_path.split('/')[-1]

        # Encode file to base64
        base64_content = base64.b64encode(file_content).decode('utf-8')

        query = f"""
            mutation {{
                add_file_to_column(item_id: {item_id}, column_id: "{column_id}", file: "{file_name}", content: "{base64_content}") {{
                    id
                    asset {{
                        id
                        name
                        url
                        file_extension
                        file_size
                    }}
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        return result["data"]["add_file_to_column"]

    def download_file(self, asset_id: int, output_path: Optional[str] = None) -> bytes:
        """Downloads a file by the asset ID.

        Args:
            asset_id: The ID of the asset to download
            output_path: Optional path to save the downloaded file

        Returns:
            The file content as bytes if no output_path is provided,
            otherwise saves the file to the specified path and returns the file content
        """
        # First, get the asset URL
        query = f"""
            query {{
                assets(ids: {asset_id}) {{
                    id
                    name
                    url
                    file_extension
                }}
            }}
        """
        self.client._query = query
        result = self.client._exec_query()

        if not result.get("data", {}).get("assets"):
            raise Exception(f"Asset with ID {asset_id} not found")

        asset = result["data"]["assets"][0]
        file_url = asset["url"]

        # Download the file
        response = requests.get(file_url, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download file: {response.status_code}")

        file_content = response.content

        # If output path is provided, save the file
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(file_content)

        return file_content