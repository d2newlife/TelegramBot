import os
import time
import util.telegram as telegram
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Ensure GOOGLE_API_KEY is set in your .env file
if not os.getenv("BOT_TOKEN"):
    raise ValueError("BOT_TOKEN environment variable not set.")

BOT_TOKEN = os.getenv("BOT_TOKEN")

def process_updates(bot_token : str, updates : list) ->int:
    # Track the highest update_id to use as the next offset
    max_update_id = 0

    if not updates:
        return 0 # No updates to process
    
    for update in updates:
        update_id = update.get('update_id')
        max_update_id = max(max_update_id, update_id)

        message = update.get('message')
        if message:
            chat_id = message.get('chat', {}).get('id')
            text = message.get('text', '')
            voice = message.get('voice', None)
            if text:
                 ############## ADD LLM HERE #################
                reply_text = f"You said: {text}" # ADD LLM HERE #
                telegram.send_message(bot_token, chat_id, reply_text)
            elif message and message.get('new_chat_member'):
                # Handle bot being added to a group (a service message)
                chat_id = message.get('chat', {}).get('id')
                welcome_text = """
                Thank you for adding me! 
                I'm an AI helper, ready to tackle your requests. 
                Send me a message to get started.
                """
                telegram.send_message(bot_token, chat_id, welcome_text)
            elif voice:
                # Down load voice message and convert to text
                voice_audio_file = telegram.download_voice_message(bot_token, message)
                #Convert audio file to text
                print(f"Voice message saved to (next step convert to text): {voice_audio_file}")
                ############## ADD LLM HERE #################
                reply_text = "Voice messages are not supported yet."
                telegram.send_message(bot_token, chat_id, reply_text)
    return max_update_id + 1

def main():
    offset = None # Start with no offset

    while True:
        messages = telegram.get_updates(BOT_TOKEN,offset)
        if messages:
            print(messages)
            offset = process_updates(BOT_TOKEN, messages)
            print(f"Next offset: {offset}")
        # Short pause to prevent hammering the API if an error occurs, sleep value is in seconds
            time.sleep(3)


if __name__ == "__main__":
    main()