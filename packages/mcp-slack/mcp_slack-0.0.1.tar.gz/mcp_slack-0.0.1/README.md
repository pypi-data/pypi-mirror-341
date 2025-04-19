# Slack MCP Server

A Model Context Protocol (MCP) server for Slack integration. This server provides tools for interacting with Slack, including sending messages, managing channels, and accessing workspace information.

## Features

- **Channel Management**: Create, list, join, and archive channels
- **Messaging**: Send messages to channels or threads, get channel history
- **Users**: Get user information and list workspace members
- **Files**: Upload files to channels
- **Reactions**: Add reactions to messages
- **Resources**: Access information about channels, users, and messages
- **Prompts**: Templates for common Slack actions

## Installation

```bash
pip install mcp-slack
```

## Configuration

Set the following environment variables:

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_APP_TOKEN="xapp-your-app-token" # Optional, needed for socket mode
```

To get these tokens:
1. Create a Slack App at https://api.slack.com/apps
2. Add the necessary permission scopes (channels:read, chat:write, etc.)
3. Install the app to your workspace
4. Get the Bot Token from the "OAuth & Permissions" page

## Usage

### Starting the server directly

```bash
mcp-slack
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
"mcp-slack": {
  "command": "uvx",
  "args": [
    "mcp-slack"
  ],
  "env": {
    "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
    "SLACK_APP_TOKEN": "xapp-your-app-token"
  }
}
```

Replace the environment variables with your actual Slack credentials.

## Available Tools

* **send_message**: Send a message to a channel or thread
* **list_channels**: List available channels in the workspace
* **get_channel_history**: Get message history for a channel
* **list_users**: List users in the workspace
* **create_channel**: Create a new channel
* **archive_channel**: Archive a channel
* **join_channel**: Join a channel
* **add_reaction**: Add a reaction to a message
* **upload_file**: Upload a file to a channel

## Available Resources

* **slack://channels**: List of all channels in the workspace
* **slack://users**: List of all users in the workspace
* **slack://channel/{channel_id}**: Information about a specific channel
* **slack://user/{user_id}**: Information about a specific user

## Available Prompts

* **create_message**: Template for creating a new message
* **create_channel**: Template for creating a new channel
* **schedule_message**: Template for scheduling a message

## Permissions Required

The Slack bot requires the following scopes:
* `channels:read` - To list and get channel information
* `channels:write` - To create and archive channels
* `chat:write` - To send messages
* `files:write` - To upload files
* `reactions:write` - To add reactions
* `users:read` - To list and get user information

## Version

0.0.1
