# Comfy Monday API

A comfortable and intuitive Python wrapper for the Monday.com GraphQL API. This library aims to simplify working with Monday.com's API by providing ready-to-use functions for common operations.

## Why Comfy Monday API?

While the official Monday.com API exists, Comfy Monday API provides:
- Pre-built methods for common operations
- Intuitive class structure mirroring Monday.com's entities
- PEP 8 compliant code
- Comprehensive type hints
- Better error handling and documentation

## Requirements

- Python 3.9+
- `requests` library

## Installation

```bash
pip install comfy-monday-api
```

## Quick Start

```python
from comfy_monday import MondayClient, MondayBoards

# Initialize the client with your API token
client = MondayClient(token="your_api_token_here")

# Create a boards manager
boards = MondayBoards(client)

# List all boards
all_boards = boards.list_boards()
for board in all_boards:
    print(f"Board ID: {board['id']}, Name: {board['name']}")
```

## API Reference

### MondayClient

The base client for making requests to the Monday.com API.

```python
from comfy_monday import MondayClient

client = MondayClient(token="your_api_token_here")
```

#### Parameters

- `token` (str): Your Monday.com API token
- `api_url` (str, optional): The Monday.com API URL. Default is "https://api.monday.com/v2"

#### Methods

- `_exec_query()`: Executes the stored GraphQL query

### MondayBoards

Handles operations related to boards, groups, items, and columns.

```python
from comfy_monday import MondayClient, MondayBoards

client = MondayClient(token="your_api_token_here")
boards = MondayBoards(client)
```

#### Methods

- `get_item_column_value(item_id, column_id)`: Get a specific column value from an item
- `update_item_column_values(item_id, board_id, column_values)`: Update column values of a specific item
- `list_boards(limit=100)`: List all accessible boards
- `list_board_groups(board_id)`: List all groups in a specific board
- `add_column_to_board(board_id, title, column_type, defaults=None)`: Add a new column to a board
- `create_board(board_name, board_kind="public", description=None)`: Create a new board
- `get_board(board_id)`: Get data about a specific board
- `get_group(board_id, group_id)`: Get data about a specific group
- `duplicate_board(board_id, board_name=None, duplicate_type="duplicate_board_with_structure")`: Duplicate a board
- `duplicate_group(board_id, group_id, group_title=None, add_to_top=False)`: Duplicate a group

### MondayItems

Handles operations related to items (pulses).

```python
from comfy_monday import MondayClient, MondayItems

client = MondayClient(token="your_api_token_here")
items = MondayItems(client)
```

#### Methods

- `list_board_items(board_id, limit=100, page=1)`: Get a list of all items on a board
- `list_group_items(board_id, group_id, limit=100)`: Get a list of all items in a group
- `search_items_by_column_value(board_id, column_id, value, limit=100)`: Search for items by column value
- `create_item(board_id, group_id, item_name, column_values=None)`: Create a new item
- `create_subitem(parent_item_id, item_name, column_values=None)`: Create a new subitem
- `get_item(item_id)`: Get data about a specific item
- `move_item_to_group(item_id, group_id)`: Move an item to a different group
- `duplicate_item(board_id, item_id, with_updates=True)`: Create a duplicate of an item
- `delete_item(item_id)`: Delete an item permanently
- `archive_item(item_id)`: Archive an item

### MondayTags

Handles operations related to tags.

```python
from comfy_monday import MondayClient, MondayTags

client = MondayClient(token="your_api_token_here")
tags = MondayTags(client)
```

#### Methods

- `create_or_get_tag(board_id, tag_name)`: Get a tag if it exists or create it if it doesn't

### MondayUsers

Handles operations related to users.

```python
from comfy_monday import MondayClient, MondayUsers

client = MondayClient(token="your_api_token_here")
users = MondayUsers(client)
```

#### Methods

- `list_users(kind=None, limit=100)`: Get a list of users
- `get_user(user_id)`: Get data about a specific user

### MondayUpdates

Handles operations related to updates.

```python
from comfy_monday import MondayClient, MondayUpdates

client = MondayClient(token="your_api_token_here")
updates = MondayUpdates(client)
```

#### Methods

- `list_updates(limit=100)`: Get a list of all updates
- `list_item_updates(item_id, limit=100)`: Get a list of updates for a specific item
- `create_update(item_id, body, parent_id=None)`: Create a new update for an item

### MondaySubscribers

Handles operations related to subscribers.

```python
from comfy_monday import MondayClient, MondaySubscribers

client = MondayClient(token="your_api_token_here")
subscribers = MondaySubscribers(client)
```

#### Methods

- `list_item_subscribers(item_id)`: Retrieves a list of item's subscribers
- `list_board_subscribers(board_id)`: Retrieves a list of subscribers of a board
- `add_board_subscribers(board_id, user_ids)`: Adds subscribers to a board
- `remove_board_subscribers(board_id, user_ids)`: Removes subscribers from a board

### MondayFiles

Handles operations related to files and assets.

```python
from comfy_monday import MondayClient, MondayFiles

client = MondayClient(token="your_api_token_here")
files = MondayFiles(client)
```

#### Methods

- `list_files(limit=100)`: Returns a list of files
- `add_file_to_update(update_id, file_path)`: Adds a file to an existing update
- `add_file_to_column(item_id, column_id, file_path)`: Adds a file to a file column value
- `download_file(asset_id, output_path=None)`: Downloads a file by the asset ID

### MondayActivities

Handles operations related to activity logs.

```python
from comfy_monday import MondayClient, MondayActivities

client = MondayClient(token="your_api_token_here")
activities = MondayActivities(client)
```

#### Methods

- `list_board_activity_logs(board_id, limit=100, page=1, from_date=None, to_date=None, user_ids=None, column_ids=None, group_ids=None, item_ids=None)`: Retrieves a list of board activity logs

### MondayTeams

Handles operations related to teams.

```python
from comfy_monday import MondayClient, MondayTeams

client = MondayClient(token="your_api_token_here")
teams = MondayTeams(client)
```

#### Methods

- `list_teams(limit=100)`: Retrieves a list of teams
- `list_team_members(team_id)`: Retrieves a list of members by team ID
- `get_team(team_id)`: Returns a team by ID

### Custom GraphQL Queries

You can execute custom GraphQL queries using the `execute_graph_query` function:

```python
from comfy_monday import MondayClient
from comfy_monday.teams import execute_graph_query

client = MondayClient(token="your_api_token_here")

query = """
    query {
        boards(limit: 5) {
            id
            name
        }
    }
"""

result = execute_graph_query(client, query)
print(result)
```

## Examples

### Working with Boards

```python
from comfy_monday import MondayClient, MondayBoards

# Initialize
client = MondayClient(token="your_api_token_here")
boards = MondayBoards(client)

# Create a new board
new_board = boards.create_board(
    board_name="Project Tasks",
    description="Tracking tasks for our new project"
)
board_id = new_board["id"]

# Add a column to the board
text_column = boards.add_column_to_board(
    board_id=board_id,
    title="Status",
    column_type="status",
    defaults={"labels": ["Done", "Working on it", "Stuck"]}
)

# Get board groups
groups = boards.list_board_groups(board_id)
group_id = groups[0]["id"]

# Duplicate the board
duplicate = boards.duplicate_board(
    board_id=board_id,
    board_name="Project Tasks - Backup"
)
```

### Working with Items

```python
from comfy_monday import MondayClient, MondayBoards, MondayItems

# Initialize
client = MondayClient(token="your_api_token_here")
boards = MondayBoards(client)
items = MondayItems(client)

# Find our board and group
board_id = 12345678  # Replace with your board ID
groups = boards.list_board_groups(board_id)
group_id = groups[0]["id"]

# Create a new item
new_item = items.create_item(
    board_id=board_id,
    group_id=group_id,
    item_name="Implement new feature",
    column_values={
        "status": {"label": "Working on it"},
        "date4": {"date": "2023-12-31"},
        "person": {"id": 1234567}  # Replace with user ID
    }
)
item_id = new_item["id"]

# Update the item
updated_item = boards.update_item_column_values(
    item_id=item_id,
    board_id=board_id,
    column_values={
        "status": {"label": "Done"},
        "date4": {"date": "2023-12-15"}
    }
)

# Move the item to another group
target_group_id = groups[1]["id"]
moved_item = items.move_item_to_group(
    item_id=item_id,
    group_id=target_group_id
)

# Get item details
item_details = items.get_item(item_id)
```

### Working with Users and Teams

```python
from comfy_monday import MondayClient, MondayUsers, MondayTeams

# Initialize
client = MondayClient(token="your_api_token_here")
users = MondayUsers(client)
teams = MondayTeams(client)

# List users
all_users = users.list_users()
for user in all_users:
    print(f"User: {user['name']} (ID: {user['id']})")

# Get a specific user
user_id = all_users[0]["id"]
user_details = users.get_user(user_id)

# List teams
all_teams = teams.list_teams()
for team in all_teams:
    print(f"Team: {team['name']} (ID: {team['id']})")

# Get team members
team_id = all_teams[0]["id"]
members = teams.list_team_members(team_id)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request