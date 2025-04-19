# Elevenlabs MCP Server

A Model Context Protocol (MCP) server for Elevenlabs integration. This server provides tools for interacting with Elevenlabs' text-to-speech API, allowing you to generate realistic speech from text, access voice libraries, and manage your account.

## Features

- **Text-to-Speech**: Convert text to high-quality speech
- **Voice Management**: List and get details about available voices
- **Model Selection**: Access different TTS models for various use cases
- **User Management**: Check subscription status and usage limits
- **History Tracking**: View your generation history
- **Resources**: Access metadata about Elevenlabs objects
- **Prompts**: Templates for common Elevenlabs workflows

## Installation

```bash
pip install mcp-elevenlabs
```

## Configuration

Set the following environment variables:

```bash
export ELEVENLABS_API_KEY="your_api_key"
export ELEVENLABS_BASE_URL="https://api.elevenlabs.io/v1" # Optional, defaults to this value
```

## Usage

### Starting the server directly

```bash
mcp-elevenlabs
```

### Using with Claude Desktop

Add the following to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "mcp-elevenlabs": {
      "command": "uvx",
      "args": [
        "mcp-elevenlabs"
      ],
      "env": {
        "ELEVENLABS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Replace the environment variables with your actual Elevenlabs credentials.

## Available Tools

* **text_to_speech**: Convert text to speech using Elevenlabs API
* **get_voices**: Get a list of available voices
* **get_voice**: Get details of a specific voice
* **get_models**: Get a list of available TTS models
* **get_user_info**: Get information about the current user's subscription
* **get_history**: Get the user's text-to-speech generation history

## Available Resources

* **elevenlabs://voices**: List of all Elevenlabs voices
* **elevenlabs://models**: List of all available TTS models
* **elevenlabs://user**: User subscription information
* **elevenlabs://history**: Generation history

## Available Prompts

* **tts_generation**: Template for generating text-to-speech
* **voice_selection**: Guide for selecting the right voice

## Example Usage

Once connected to Claude, you can use the Elevenlabs MCP server to generate speech:

```
Convert this text to speech: "Hello, world! This is a test of the Elevenlabs text-to-speech system."
```

Claude will use the text_to_speech tool to generate speech from your text.

To get information about available voices:

```
What voices are available in Elevenlabs?
```

Claude will use the get_voices tool to retrieve and display the list of voices.

## Version

0.0.1
