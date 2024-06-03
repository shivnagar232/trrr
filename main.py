import os
import time
import logging
import subprocess
from pyrogram import Client, filters, enums
from config import session_string, allowed_groups, owner_id, extract_links
from downloader import check_url_patterns_async, fetch_download_link_async, get_formatted_size_async, my_headers

API_ID = "19748984"  # Replace with your API_ID from config.py
API_HASH = "2141e30f96dfbd8c46fbb5ff4b197004"  # Replace with your API_HASH from config.py
BOT_TOKEN = "6399306217:AAFpGkkyZSOZoQJuMg5bR6AV4P-OmbFs1a4"  # Replace with your BOT_TOKEN from config.py

app = Client(
    name="trbx",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)

logging.basicConfig(level=logging.INFO)

# Function to download using aria2c and get downloaded file path
async def download_with_aria2c(download_link):
    try:
        download_process = subprocess.Popen(['aria2c', '-x', '16', '-s', '16', download_link], stdout=subprocess.PIPE)
        stdout, stderr = download_process.communicate()
        if download_process.returncode == 0:
            # Parse stdout or extract downloaded file path
            # For simplicity, assuming file is downloaded to current directory
            downloaded_file = find_downloaded_file()
            return downloaded_file
        else:
            logging.error(f"aria2c process returned non-zero exit code: {download_process.returncode}")
            return None
    except Exception as e:
        logging.error(f"Error in downloading with aria2c: {e}")
        return None

# Function to find downloaded file in current directory
def find_downloaded_file():
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir):
        if filename.startswith("file_"):  # Adjust filename prefix as per your download scenario
            return os.path.join(current_dir, filename)
    return None

# Function to send document back to user
async def send_document_to_user(chat_id, file_path, caption):
    try:
        await app.send_document(chat_id, file_path, caption=caption)
        return True
    except Exception as e:
        logging.error(f"Error in sending document to user: {e}")
        return False

@app.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text("⚠️ Forbidden!\nFor groups access.\nContact @DTMK_C", quote=True)
        return
    else:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text(
            "Hello! I'm Terabox link Bypass Bot. Send me a link to bypass.\n"
            "Owner: @DTMK_C\n"
            "Eg:- `https://teraboxapp.com/s/1Ykohv-bhT4SJJEgyDMeS-A`", quote=True)

@app.on_message(filters.command("ping"))
async def ping(client, message):
    if str(message.from_user.id) != owner_id:
        return
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    start_time = time.time()
    sent_message = await message.reply_text("Pong!", quote=True)
    end_time = time.time()
    time_taken = end_time - start_time
    await sent_message.edit_text(f"Pong!\nTime Taken: {time_taken:.2f} seconds")

async def format_message(link_data):
    file_name = link_data["server_filename"]
    file_size = await get_formatted_size_async(link_data["size"])
    download_link = link_data["dlink"]
    return f"┎ <b>Title</b>: `{file_name}`\n┠ <b>Size</b>: `{file_size}`\n┖ <b>Link</b>: <a href={download_link}>Link</a>"

@app.on_message(filters.regex(
    pattern=r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"))
async def link_handler(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text("⚠️ Forbidden! For groups access.\nContact @DTMK_C", quote=True)
        return
    else:
        start_time = time.time()
        urls = extract_links(message.text) + extract_links(message.caption)
        if not urls:
            await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
            await message.reply_text("⚠️ No valid URLs found!", quote=True)
            return
        try:
            for url in urls:
                if not await check_url_patterns_async(url):
                    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                    await message.reply_text("⚠️ Not a valid Terabox URL!", quote=True)
                    continue

                await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                process_url = await message.reply_text("🔎 Processing URL...", quote=True)
                link_data = await fetch_download_link_async(url)

                end_time = time.time()
                time_taken = end_time - start_time
                await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)

                link_message = "\n\n".join([await format_message(link) for link in link_data])
                download_message = (
                    f"🔗 <b>Link Bypassed!</b>\n\n{link_message}\n\n<b>Time Taken</b>: {time_taken:.2f} seconds"
                )
                await process_url.edit_text(download_message)

                # Example using aria2c for download
                if link_data:
                    download_link = link_data[0]["dlink"]  # Assuming first link in list
                    downloaded_file = await download_with_aria2c(download_link)
                    if downloaded_file:
                        caption = "Downloaded file"
                        await send_document_to_user(message.chat.id, downloaded_file, caption)
                    else:
                        await client.send_message(message.chat.id, "Failed to download.")

        except Exception as e:
            await message.reply_text(f"Error: {e}", quote=True)

# run the application
app.run()
