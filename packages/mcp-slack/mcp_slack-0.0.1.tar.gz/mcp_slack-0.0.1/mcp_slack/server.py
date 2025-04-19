# server.py
import sys
import os
import json
from typing import Dict, List, Optional, Any, Union
import httpx
from mcp.server.fastmcp import FastMCP
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Create an MCP server
mcp = FastMCP("Slack MCP")

# Environment variables for Slack configuration
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# Check if environment variables are set
if not SLACK_BOT_TOKEN:
    print("Warning: Slack environment variables not fully configured. Set SLACK_BOT_TOKEN.", file=sys.stderr)

# Initialize Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN) if SLACK_BOT_TOKEN else None

# Helper function for response formatting
def format_slack_response(response, error=None):
    """Format Slack API response for readability."""
    if error:
        return f"Error: {error}"
    
    return json.dumps(response, indent=2)

# === TOOLS ===

@mcp.tool()
async def send_message(channel: str, text: str, thread_ts: str = None) -> str:
    """
    Send a message to a Slack channel or thread.
    
    Args:
        channel: Channel ID or name (e.g., C01234567 or #general)
        text: Message text
        thread_ts: Optional thread timestamp to reply in a thread
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        # Handle channel names with # prefix
        if channel.startswith('#'):
            channel = channel[1:]
            
            # Find channel ID from name
            channels_response = slack_client.conversations_list()
            for ch in channels_response["channels"]:
                if ch["name"] == channel:
                    channel = ch["id"]
                    break
        
        # Prepare request parameters
        params = {
            "channel": channel,
            "text": text
        }
        
        if thread_ts:
            params["thread_ts"] = thread_ts
            
        # Send message
        response = slack_client.chat_postMessage(**params)
        
        return format_slack_response({
            "status": "success",
            "channel": channel,
            "ts": response["ts"],
            "message": text
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to send message: {str(e)}")

@mcp.tool()
async def list_channels(limit: int = 100, exclude_archived: bool = True) -> str:
    """
    List channels in the workspace.
    
    Args:
        limit: Maximum number of channels to return (default: 100)
        exclude_archived: Whether to exclude archived channels (default: True)
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        response = slack_client.conversations_list(
            limit=limit,
            exclude_archived=exclude_archived
        )
        
        channels = [{
            "id": channel["id"],
            "name": channel["name"],
            "is_private": channel.get("is_private", False),
            "member_count": channel.get("num_members", 0),
            "topic": channel.get("topic", {}).get("value", ""),
            "purpose": channel.get("purpose", {}).get("value", "")
        } for channel in response["channels"]]
        
        return format_slack_response({
            "status": "success",
            "count": len(channels),
            "channels": channels
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to list channels: {str(e)}")

@mcp.tool()
async def get_channel_history(channel: str, limit: int = 10) -> str:
    """
    Get message history for a channel.
    
    Args:
        channel: Channel ID or name
        limit: Maximum number of messages to return (default: 10)
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        # Handle channel names with # prefix
        if channel.startswith('#'):
            channel = channel[1:]
            
            # Find channel ID from name
            channels_response = slack_client.conversations_list()
            for ch in channels_response["channels"]:
                if ch["name"] == channel:
                    channel = ch["id"]
                    break
        
        response = slack_client.conversations_history(
            channel=channel,
            limit=limit
        )
        
        messages = [{
            "user": msg.get("user", ""),
            "text": msg.get("text", ""),
            "ts": msg.get("ts", ""),
            "thread_ts": msg.get("thread_ts", None),
            "has_replies": msg.get("reply_count", 0) > 0
        } for msg in response["messages"]]
        
        return format_slack_response({
            "status": "success",
            "channel": channel,
            "count": len(messages),
            "messages": messages
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to get channel history: {str(e)}")

@mcp.tool()
async def list_users(limit: int = 100) -> str:
    """
    List users in the workspace.
    
    Args:
        limit: Maximum number of users to return (default: 100)
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        response = slack_client.users_list(limit=limit)
        
        users = [{
            "id": user["id"],
            "name": user["name"],
            "real_name": user.get("real_name", ""),
            "display_name": user.get("profile", {}).get("display_name", ""),
            "email": user.get("profile", {}).get("email", ""),
            "is_bot": user.get("is_bot", False),
            "is_admin": user.get("is_admin", False)
        } for user in response["members"]]
        
        return format_slack_response({
            "status": "success",
            "count": len(users),
            "users": users
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to list users: {str(e)}")

@mcp.tool()
async def create_channel(name: str, is_private: bool = False) -> str:
    """
    Create a new channel.
    
    Args:
        name: Channel name (lowercase, no spaces or special chars except - and _)
        is_private: Whether the channel should be private (default: False)
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        # Clean channel name - Slack requires lowercase, no spaces or special chars
        name = name.lower().replace(' ', '-')
        
        response = slack_client.conversations_create(
            name=name,
            is_private=is_private
        )
        
        channel = response["channel"]
        
        return format_slack_response({
            "status": "success",
            "id": channel["id"],
            "name": channel["name"],
            "is_private": channel.get("is_private", False),
            "created": channel.get("created", 0)
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to create channel: {str(e)}")

@mcp.tool()
async def archive_channel(channel: str) -> str:
    """
    Archive a channel.
    
    Args:
        channel: Channel ID or name
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        # Handle channel names with # prefix
        if channel.startswith('#'):
            channel = channel[1:]
            
            # Find channel ID from name
            channels_response = slack_client.conversations_list()
            for ch in channels_response["channels"]:
                if ch["name"] == channel:
                    channel = ch["id"]
                    break
        
        response = slack_client.conversations_archive(channel=channel)
        
        return format_slack_response({
            "status": "success",
            "channel": channel,
            "archived": True
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to archive channel: {str(e)}")

@mcp.tool()
async def join_channel(channel: str) -> str:
    """
    Join a channel.
    
    Args:
        channel: Channel ID or name
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        # Handle channel names with # prefix
        if channel.startswith('#'):
            channel = channel[1:]
            
            # Find channel ID from name
            channels_response = slack_client.conversations_list()
            for ch in channels_response["channels"]:
                if ch["name"] == channel:
                    channel = ch["id"]
                    break
        
        response = slack_client.conversations_join(channel=channel)
        
        return format_slack_response({
            "status": "success",
            "channel": response["channel"]["id"],
            "name": response["channel"]["name"]
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to join channel: {str(e)}")

@mcp.tool()
async def add_reaction(channel: str, timestamp: str, reaction: str) -> str:
    """
    Add a reaction to a message.
    
    Args:
        channel: Channel ID where the message is
        timestamp: Timestamp of the message
        reaction: Reaction name (without the colons, e.g., 'thumbsup')
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        # Remove colons if they're included
        reaction = reaction.strip(':')
        
        response = slack_client.reactions_add(
            channel=channel,
            timestamp=timestamp,
            name=reaction
        )
        
        return format_slack_response({
            "status": "success",
            "reaction": reaction,
            "added": True
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to add reaction: {str(e)}")

@mcp.tool()
async def upload_file(channel: str, file_path: str, initial_comment: str = None) -> str:
    """
    Upload a file to a channel.
    
    Args:
        channel: Channel ID or name
        file_path: Path to the file to upload
        initial_comment: Optional text to accompany the file
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        # Handle channel names with # prefix
        if channel.startswith('#'):
            channel = channel[1:]
            
            # Find channel ID from name
            channels_response = slack_client.conversations_list()
            for ch in channels_response["channels"]:
                if ch["name"] == channel:
                    channel = ch["id"]
                    break
        
        # Check if file exists
        if not os.path.exists(file_path):
            return format_slack_response(None, f"File not found: {file_path}")
        
        # Prepare request parameters
        params = {
            "channels": channel,
            "file": file_path
        }
        
        if initial_comment:
            params["initial_comment"] = initial_comment
            
        # Upload file
        response = slack_client.files_upload_v2(**params)
        
        return format_slack_response({
            "status": "success",
            "channel": channel,
            "file_id": response["file"]["id"],
            "name": response["file"]["name"],
            "url": response["file"].get("url_private", "")
        })
        
    except SlackApiError as e:
        return format_slack_response(None, f"Failed to upload file: {str(e)}")

# === RESOURCES ===

@mcp.resource("slack://channels")
async def get_all_channels() -> str:
    """Get a list of all Slack channels."""
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        response = slack_client.conversations_list()
        return json.dumps(response, indent=2)
    except SlackApiError as e:
        return f"Error retrieving channels: {str(e)}"

@mcp.resource("slack://users")
async def get_all_users() -> str:
    """Get a list of all Slack users."""
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        response = slack_client.users_list()
        return json.dumps(response, indent=2)
    except SlackApiError as e:
        return f"Error retrieving users: {str(e)}"

@mcp.resource("slack://channel/{channel_id}")
async def get_channel_info(channel_id: str) -> str:
    """
    Get information about a specific Slack channel.
    
    Args:
        channel_id: ID of the channel (e.g., C01234567)
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        response = slack_client.conversations_info(channel=channel_id)
        return json.dumps(response, indent=2)
    except SlackApiError as e:
        return f"Error retrieving channel info: {str(e)}"

@mcp.resource("slack://user/{user_id}")
async def get_user_info(user_id: str) -> str:
    """
    Get information about a specific Slack user.
    
    Args:
        user_id: ID of the user (e.g., U01234567)
    """
    if not slack_client:
        return "Error: Slack client not initialized. Check SLACK_BOT_TOKEN."
    
    try:
        response = slack_client.users_info(user=user_id)
        return json.dumps(response, indent=2)
    except SlackApiError as e:
        return f"Error retrieving user info: {str(e)}"

# === PROMPTS ===

@mcp.prompt("create_message")
def create_message_prompt(channel: str = None, text: str = None):
    """
    A prompt template for creating a new message in Slack.
    
    Args:
        channel: Channel name or ID
        text: Message text
    """
    if all([channel, text]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me send a message to the Slack channel {channel} with the following content:\n\n{text}"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to send a message to a Slack channel. Please help me formulate it clearly and professionally."
                    }
                }
            ]
        }

@mcp.prompt("create_channel")
def create_channel_prompt(name: str = None, purpose: str = None, is_private: bool = False):
    """
    A prompt template for creating a new channel in Slack.
    
    Args:
        name: Channel name
        purpose: Channel purpose
        is_private: Whether the channel should be private
    """
    channel_type = "private" if is_private else "public"
    
    if all([name, purpose]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me create a new {channel_type} Slack channel with these details:\n\nName: {name}\nPurpose: {purpose}"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"I need to create a new {channel_type} Slack channel. Please help me with the required details."
                    }
                }
            ]
        }

@mcp.prompt("schedule_message")
def schedule_message_prompt(channel: str = None, text: str = None, time: str = None):
    """
    A prompt template for scheduling a message in Slack.
    
    Args:
        channel: Channel name or ID
        text: Message text
        time: When to send the message (e.g., "tomorrow at 9am")
    """
    if all([channel, text, time]):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me schedule a message in Slack channel {channel} for {time} with the following content:\n\n{text}"
                    }
                }
            ]
        }
    else:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": "I need to schedule a message in Slack. Please help me with the timing and content."
                    }
                }
            ]
        }

if __name__ == "__main__":
    print("Starting Slack MCP server...", file=sys.stderr)
    mcp.run()
