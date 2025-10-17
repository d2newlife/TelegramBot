import requests
import time
import json
import os
from typing import Any, Dict, Optional

TELEGRAM_API_BASE = "https://api.telegram.org/bot"
TELEGRAM_DOWNLOAD_BASE = "https://api.telegram.org/file/bot"

def get_updates(bot_token : str, offset:int | None=None)->list:
    """Fetches new messages (updates) from the Telegram API."""
    try:
        telegram_api = f"{TELEGRAM_API_BASE}{bot_token}/"
        url = telegram_api + "getUpdates"
        params = {
            'timeout': 10,  # Long poll timeout (wait up to 10 seconds for a new message)
            'offset': offset # Start reading from this update ID
        }
        # Use a longer timeout for polling, matching the 'timeout' parameter + a buffer
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json().get('result', [])
    except json.JSONDecodeError as e:
        print(f"Error: Server response was not valid JSON. {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error getting updates: {e}. Retrying in 5 seconds...")
        time.sleep(5)
        return []

def send_message(bot_token : str, chat_id :str, text : str)-> dict[str, Any]:
    """Sends a text message to a specified chat ID."""
    try:
        telegram_api = f"{TELEGRAM_API_BASE}{bot_token}/"
        url = telegram_api + "sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        # Use a short timeout for network robustness
        response = requests.post(url, data=payload, timeout=5)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Sent reply to chat {chat_id}: '{text}'")
        return response.json()
    except json.JSONDecodeError as e:
        print(f"Error: Server response was not valid JSON. {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None
    
def download_voice_message(bot_token: str, update_message: Dict[str, Any], download_path: str = "audio") -> Optional[str]:
    if 'voice' not in update_message:
        print("Error: The provided message dictionary does not contain a 'voice' object.")
        return None

    voice_data = update_message['voice']
    file_id = voice_data.get('file_id')
    mime_type = voice_data.get('mime_type', 'audio/ogg')
    # Extract the common extension from the MIME type (e.g., 'ogg' from 'audio/ogg')
    file_extension = mime_type.split('/')[-1] if '/' in mime_type else 'ogg'

    if not file_id:
        print("Error: Voice data is missing 'file_id'.")
        return None
    
    # --- Step 1: Get the File Path ---
    try:
        get_file_url = f"{TELEGRAM_API_BASE}{bot_token}/getFile"
        params = {'file_id': file_id}
        
        # Request the file path from Telegram
        response = requests.get(get_file_url, params=params)
        response.raise_for_status()
        file_info = response.json()
        
        if not file_info.get('ok'):
            print(f"Error calling getFile: {file_info.get('description', 'Unknown error')}")
            return None
        
        # The file_path is needed for the download URL
        file_path = file_info['result']['file_path']
        
    except requests.exceptions.RequestException as e:
        print(f"Network error while getting file path: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON response for getFile.")
        return None
    except KeyError:
        print("Error: 'file_path' missing in getFile response.")
        return None
    
    # --- Step 2: Download the File ---
    download_url = f"{TELEGRAM_DOWNLOAD_BASE}{bot_token}/{file_path}"
    
    # Create the download directory if it doesn't exist
    os.makedirs(download_path, exist_ok=True)
    
    # Create a unique filename for the downloaded file
    chat_id = update_message['chat']['id']
    message_id = update_message['message_id']
    local_filename = os.path.join(download_path, f"voice_{chat_id}_{message_id}.{file_extension}")

    try:
        # Stream the download to handle potentially large files
        download_response = requests.get(download_url, stream=True)
        download_response.raise_for_status()
        
        # Write the file content in chunks
        with open(local_filename, 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        print(f"Successfully downloaded voice message to: {local_filename}")
        return local_filename

    except requests.exceptions.RequestException as e:
        print(f"Network error during file download: {e}")
        return None