import os
from pyrogram import Client, filters
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your API details from the .env file
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# Create a Pyrogram client instance
app = Client("user_session", api_id=api_id, api_hash=api_hash)

# Folder to store the downloaded songs
DOWNLOAD_FOLDER = 'songs/'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

async def download_songs(channel_id):
    # Fetch messages from the channel
    async for message in app.get_chat_history(channel_id):
        # Check if the message contains audio
        if message.audio:
            file_name = message.audio.file_name or f"song_{message.message_id}.mp3"
            print(f"Downloading {file_name}...")
            await app.download_media(message.audio, file_name=os.path.join(DOWNLOAD_FOLDER, file_name))
        # Check if the message contains a document (audio file)
        elif message.document and message.document.mime_type.startswith("audio/"):
            file_name = message.document.file_name or f"song_{message.message_id}.mp3"
            print(f"Downloading {file_name}...")
            await app.download_media(message.document, file_name=os.path.join(DOWNLOAD_FOLDER, file_name))

@app.on_message(filters.command("download"))
async def download_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a valid channel ID or username.")
        return

    channel_id = message.command[1]
    await message.reply_text(f"Starting to download songs from channel: {channel_id}")
    await download_songs(channel_id)
    await message.reply_text("Download complete!")

if __name__ == "__main__":
    app.run()
