import logging
import random
import string
from sys import stdin, stdout
import json
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from gj_meta_mcp.digital_human_generator import DigitalHumanGenerator

load_dotenv()
app_id = os.getenv('APP_ID')
secret_key = os.getenv('SECRET_KEY')
authorize_url = os.getenv('AUTHORIZE_URL')
authorize_text = os.getenv('AUTHORIZE_TEXT')

if not app_id or not secret_key:
    raise ValueError("APP_ID and SECRET_KEY environment variable is required")

if not authorize_url or not authorize_text:
    raise ValueError("AUTHORIZE_URL and AUTHORIZE_TEXT environment variable is required")

# Configure stdin and stdout encoding
stdin.reconfigure(encoding='utf-8')
stdout.reconfigure(encoding='utf-8')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP("create-meta-human")


@mcp.tool("mcp_list_tools")
async def mcp_list_tools():
    """List all available tools and their parameters"""
    return {
        "tools": [
            {
                "name": "create-meta-human",
                "description": "Create a digital human mp4 video based on an existing video and audio",
                "parameters": {
                    "video_url": {
                        "type": "string",
                        "description": "Original video URL in mp4 format",
                        "required": True
                    },
                    "audio_url": {
                        "type": "string",
                        "description": "Audio URL in wav format",
                        "required": True
                    },
                }
            }
        ]
    }


def generate_random_string(length):
    """Generate a random string of specified length"""
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


@mcp.tool('create meta human')
async def create_meta_human(video_url: str, audio_url: str):
    """
    Create a digital human mp4 video using provided audio and video URLs
    
    Args:
        video_url (str): Original video URL
        audio_url (str): Audio URL
        
    Returns:
        list: List of TextContent objects containing the result
    """
    try:
        generator = DigitalHumanGenerator()
        # Generate random names
        name = f"meta_{generate_random_string(8)}"
        video_name = f"video_{generate_random_string(8)}"

        video_url = await generator.generate_digital_human(
            name=name,
            video_name=video_name,
            video_url=video_url,
            audio_url=audio_url,
            app_id=app_id,
            secret_key=secret_key,
            authorize_url=authorize_url,
            authorize_text=authorize_text
        )
        # Return result
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "error": None,
                    "video_url": video_url
                }, ensure_ascii=False)
            )
        ]
    except Exception as e:
        error_msg = f"Failed to generate digital human video: {str(e)}"
        logger.error(error_msg)
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": error_msg,
                    "video_url": None
                }, ensure_ascii=False)
            )
        ]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
