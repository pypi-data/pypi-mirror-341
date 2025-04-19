# server.py
import sys
import os
import json
import httpx
import base64
from io import BytesIO
from typing import Dict, List, Optional, Any, Union
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Elevenlabs MCP")

# Environment variables for Elevenlabs configuration
ELEVENLABS_BASE_URL = os.environ.get("ELEVENLABS_BASE_URL", "https://api.elevenlabs.io/v1")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Check if environment variables are set
if not ELEVENLABS_API_KEY:
    print("Warning: Elevenlabs environment variables not fully configured. Set ELEVENLABS_API_KEY.", file=sys.stderr)

# Helper function for API requests
async def make_elevenlabs_request(method: str, endpoint: str, data: Dict = None, params: Dict = None, stream: bool = False) -> Union[Dict, bytes]:
    """
    Make a request to the Elevenlabs API.
    
    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint (without base URL)
        data: Data to send (for POST/PUT)
        params: Query parameters (for GET)
        stream: Whether to stream the response (for audio)
    
    Returns:
        Response from Elevenlabs API as dictionary or bytes
    """
    url = f"{ELEVENLABS_BASE_URL}{endpoint}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "application/json"
    }
    
    if data and not stream:
        headers["Content-Type"] = "application/json"
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                if stream:
                    headers["Accept"] = "audio/mpeg"
                    response = await client.post(url, headers=headers, json=data)
                else:
                    response = await client.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            if stream or "audio" in response.headers.get("Content-Type", ""):
                return response.content
            
            return response.json()
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error: {e.response.status_code}"
            try:
                error_json = e.response.json()
                error_msg = f"{error_msg} - {error_json.get('detail', '')}"
            except:
                pass
            
            return {
                "error": True,
                "status_code": e.response.status_code,
                "message": error_msg
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }

# === TOOLS ===

@mcp.tool()
async def text_to_speech(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", model_id: str = "eleven_monolingual_v1") -> str:
    """
    Convert text to speech using Elevenlabs API.
    
    Args:
        text: The text to convert to speech
        voice_id: The ID of the voice to use. Defaults to 'Rachel' voice
        model_id: The ID of the model to use. Defaults to 'eleven_monolingual_v1'
    
    Returns:
        Base64 encoded audio data with appropriate metadata
    """
    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    result = await make_elevenlabs_request("POST", f"/text-to-speech/{voice_id}", data=data, stream=True)
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error generating speech: {result.get('message', 'Unknown error')}"
    
    # Convert binary audio to base64
    audio_base64 = base64.b64encode(result).decode('utf-8')
    return json.dumps({
        "audio_data": audio_base64,
        "format": "audio/mpeg",
        "voice_id": voice_id,
        "model_id": model_id
    })

@mcp.tool()
async def get_voices() -> str:
    """
    Get a list of available voices from Elevenlabs.
    """
    result = await make_elevenlabs_request("GET", "/voices")
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving voices: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    formatted_voices = []
    for voice in result.get("voices", []):
        formatted_voices.append({
            "voice_id": voice.get("voice_id"),
            "name": voice.get("name"),
            "category": voice.get("category"),
            "description": voice.get("description"),
            "preview_url": voice.get("preview_url")
        })
    
    return json.dumps(formatted_voices, indent=2)

@mcp.tool()
async def get_voice(voice_id: str) -> str:
    """
    Get details of a specific Elevenlabs voice.
    
    Args:
        voice_id: The ID of the voice to retrieve
    """
    result = await make_elevenlabs_request("GET", f"/voices/{voice_id}")
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving voice: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    formatted_voice = {
        "voice_id": result.get("voice_id"),
        "name": result.get("name"),
        "category": result.get("category"),
        "description": result.get("description"),
        "samples": [s.get("file_name") for s in result.get("samples", [])]
    }
    
    return json.dumps(formatted_voice, indent=2)

@mcp.tool()
async def get_models() -> str:
    """
    Get a list of available TTS models from Elevenlabs.
    """
    result = await make_elevenlabs_request("GET", "/models")
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving models: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    formatted_models = []
    for model in result:
        formatted_models.append({
            "model_id": model.get("model_id"),
            "name": model.get("name"),
            "description": model.get("description"),
            "language": model.get("language")
        })
    
    return json.dumps(formatted_models, indent=2)

@mcp.tool()
async def get_user_info() -> str:
    """
    Get information about the current user's subscription and usage.
    """
    result = await make_elevenlabs_request("GET", "/user/subscription")
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving user information: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    formatted_info = {
        "tier": result.get("tier"),
        "character_count": result.get("character_count"),
        "character_limit": result.get("character_limit"),
        "can_extend_character_limit": result.get("can_extend_character_limit"),
        "allowed_to_extend_character_limit": result.get("allowed_to_extend_character_limit"),
        "next_character_count_reset_unix": result.get("next_character_count_reset_unix")
    }
    
    return json.dumps(formatted_info, indent=2)

@mcp.tool()
async def get_history(page_size: int = 10) -> str:
    """
    Get the user's text-to-speech generation history.
    
    Args:
        page_size: Number of history items to retrieve (default: 10)
    """
    params = {"page_size": page_size}
    result = await make_elevenlabs_request("GET", "/history", params=params)
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving history: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    formatted_history = []
    for item in result.get("history", []):
        formatted_history.append({
            "history_item_id": item.get("history_item_id"),
            "request_id": item.get("request_id"),
            "voice_id": item.get("voice_id"),
            "voice_name": item.get("voice_name"),
            "text": item.get("text"),
            "date_unix": item.get("date_unix"),
            "character_count_change_from": item.get("character_count_change_from"),
            "character_count_change_to": item.get("character_count_change_to"),
            "content_type": item.get("content_type")
        })
    
    return json.dumps(formatted_history, indent=2)

# === RESOURCES ===

@mcp.resource("elevenlabs://voices")
async def get_voices_resource() -> str:
    """Get a list of all available Elevenlabs voices."""
    result = await make_elevenlabs_request("GET", "/voices")
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving voices: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("elevenlabs://models")
async def get_models_resource() -> str:
    """Get a list of all available Elevenlabs models."""
    result = await make_elevenlabs_request("GET", "/models")
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving models: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("elevenlabs://user")
async def get_user_resource() -> str:
    """Get information about the current user's subscription."""
    result = await make_elevenlabs_request("GET", "/user/subscription")
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving user information: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

@mcp.resource("elevenlabs://history")
async def get_history_resource() -> str:
    """Get the user's text-to-speech generation history."""
    result = await make_elevenlabs_request("GET", "/history")
    
    if isinstance(result, dict) and result.get("error"):
        return f"Error retrieving history: {result.get('message', 'Unknown error')}"
    
    # Format the result in a readable way
    return json.dumps(result, indent=2)

# === PROMPTS ===

@mcp.prompt("tts_generation")
def tts_generation_prompt(text: str = None, voice_id: str = None, model_id: str = None):
    """
    A prompt template for generating text-to-speech with Elevenlabs.
    
    Args:
        text: Text to convert to speech
        voice_id: ID of the voice to use
        model_id: ID of the model to use
    """
    params = []
    if text:
        params.append(f"Text: {text}")
    if voice_id:
        params.append(f"Voice ID: {voice_id}")
    if model_id:
        params.append(f"Model ID: {model_id}")
    
    if params:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Please help me generate speech using Elevenlabs with these parameters:\n\n{chr(10).join(params)}"
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
                        "text": "I'd like to convert some text to speech using Elevenlabs. Please help me understand the parameters I need to provide."
                    }
                }
            ]
        }

@mcp.prompt("voice_selection")
def voice_selection_prompt():
    """
    A prompt template for helping users select an appropriate voice.
    """
    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": "I need help selecting the right voice for my text-to-speech project. Could you guide me through the available Elevenlabs voices and help me choose based on my requirements?"
                }
            }
        ]
    }

if __name__ == "__main__":
    print("Starting Elevenlabs MCP server...", file=sys.stderr)
    mcp.run()
