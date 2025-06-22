# EthioMart_NER_Project/scripts/scraper/telegram_scraper.py

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeVideo,
    MessageMediaDocument,
    MessageMediaPhoto
)
import asyncio
import os
import json
from datetime import datetime
import sys

# Add the project root to the Python path to import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import config # Import configuration from config.py

# --- Configuration (loaded from config.py) ---
API_ID = config.API_ID
API_HASH = config.API_HASH
PHONE_NUMBER = config.PHONE_NUMBER
SESSION_NAME = config.SESSION_NAME

# List of Telegram channel usernames or links to scrape
# IMPORTANT: Replace with actual Ethiopian e-commerce Telegram channels you identified
CHANNELS = [
    '@helloomarketethiopia',
    '@ethio_brand_collection',
    '@ZemenExpress',
    '@modernshoppingcenter',
    '@Shewabrand',
    '@Fashiontera',
    '@qnashcom',
    '@MerttEka',
    '@classybrands'
]

# Output file for all combined messages (relative to project root)
COMBINED_RAW_JSON_PATH = os.path.join(config.PREPROCESSED_DATA_DIR, config.COMBINED_RAW_MESSAGES_FILE)
# Directory for Telethon session files
RAW_DATA_SESSION_DIR = config.RAW_DATA_DIR

# Ensure output directories exist
os.makedirs(os.path.dirname(COMBINED_RAW_JSON_PATH), exist_ok=True)
os.makedirs(RAW_DATA_SESSION_DIR, exist_ok=True)


async def connect_and_scrape():
    client = TelegramClient(os.path.join(RAW_DATA_SESSION_DIR, SESSION_NAME), API_ID, API_HASH)

    print("Connecting to Telegram...")
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.send_code_request(PHONE_NUMBER)
            # Handle 2FA password if enabled
            from telethon import errors
            try:
                await client.sign_in(PHONE_NUMBER, input('Enter the code from Telegram: '))
            except errors.SessionPasswordNeededError:
                await client.sign_in(password=input('Two-step verification enabled. Enter your password: '))
        print("Connected to Telegram!")
    except Exception as e:
        print(f"Error connecting to Telegram: {e}")
        return

    # Initialize a single list to hold all messages from all channels
    all_combined_messages = []
    
    for channel_id in CHANNELS:
        print(f"\nScraping channel: {channel_id}")
        try:
            entity = await client.get_entity(channel_id)
            offset_id = 0
            limit = 100 # Max limit per API call, pagination handles fetching all
            channel_messages_count = 0 # To track messages fetched for current channel

            while True:
                history = await client(GetHistoryRequest(
                    peer=entity,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                messages = history.messages
                if not messages:
                    break

                for message in messages:
                    message_data = {
                        'id': message.id,
                        'channel_id': entity.id, # Include channel ID for traceability
                        'channel_name': entity.title, # Include channel name for traceability
                        'date': message.date.isoformat(),
                        'sender_id': message.sender_id,
                        'message': message.message,
                        'views': message.views,
                        'forwards': message.forwards,
                        'replies_count': message.replies.replies if message.replies else 0,
                        'media_type': None,
                        'file_name': None,
                        'file_path': None # This will remain None as files are not downloaded
                    }

                    # Handle media (images, documents) - ONLY RECORD METADATA, DO NOT DOWNLOAD
                    if message.media:
                        message_data['media_type'] = type(message.media).__name__

                        if isinstance(message.media, MessageMediaDocument) and message.media.document:
                            found_filename = False
                            for attr in message.media.document.attributes:
                                if isinstance(attr, DocumentAttributeFilename):
                                    message_data['file_name'] = attr.file_name
                                    found_filename = True
                                    break
                                elif isinstance(attr, DocumentAttributeVideo):
                                    message_data['media_type'] = 'VideoDocument' # More specific type
                                    # You could add message_data['video_duration'] = attr.duration, etc. if needed
                            if not found_filename:
                                # If no specific filename attribute, assign a generic name
                                message_data['file_name'] = 'unknown_document_file'

                            message_data['file_path'] = "Not Downloaded (document/video)"

                        elif isinstance(message.media, MessageMediaPhoto):
                            message_data['media_type'] = 'Photo'
                            message_data['file_name'] = f"photo_{message.id}.jpg" # Assign a generic name for photos
                            message_data['file_path'] = "Not Downloaded (photo)"
                        else:
                            # Catch any other unhandled media types (e.g., sticker, gif)
                            pass 

                    all_combined_messages.append(message_data)
                
                offset_id = messages[-1].id
                channel_messages_count += len(messages)
                print(f"  Fetched {len(messages)} messages. Total for {entity.title}: {channel_messages_count}")
                await asyncio.sleep(1) # Simple delay to avoid hitting rate limits

            print(f"Finished scraping {channel_messages_count} messages from {entity.title}")

        except Exception as e:
            print(f"Error scraping channel {channel_id}: {e}")

    await client.disconnect()
    print("\nDisconnected from Telegram.")
    print(f"Total messages scraped from all channels: {len(all_combined_messages)}")

    # Save all collected messages to a single JSON file
    try:
        with open(COMBINED_RAW_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(all_combined_messages, f, ensure_ascii=False, indent=4)
        print(f"All messages saved to {COMBINED_RAW_JSON_PATH}")
    except Exception as e:
        print(f"Error saving combined JSON file: {e}")

if __name__ == '__main__':
    asyncio.run(connect_and_scrape())