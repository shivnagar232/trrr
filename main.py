import os
import time
import logging
import requests
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


@app.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text("⚠️ Forbidden!\nFor groups access.\nContact @devggn", quote=True)
        return
    else:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text(
            "Hello! I'm Terabox link Bypass Bot. Send me a link to bypass.\n"
            "Owner: @devggn\n"
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
    formatted_messages = []
    for link in link_data:
        file_name = link["server_filename"]
        file_size = await get_formatted_size_async(link["size"])
        download_link = link["dlink"]
        formatted_messages.append(
            f"┎ <b>Title</b>: `{file_name}`\n┠ <b>Size</b>: `{file_size}`\n┖ <b>Link</b>: <a href={download_link}>Link</a>"
        )
    return formatted_messages


async def download_file(download_link):
    file_response = requests.get(download_link)
    if file_response.status_code == 200:
        file_name = "downloaded_file.ext"  # Adjust the filename and extension as needed
        with open(file_name, "wb") as f:
            f.write(file_response.content)
        return file_name
    else:
        raise Exception(f"Failed to download file: {file_response.status_code}")


@app.on_message(filters.regex(
    pattern=r"[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"))
async def link_handler(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text("⚠️ Forbidden! For groups access.\nContact @devggn", quote=True)
        return
    else:
        try:
            start_time = time.time()
            urls = extract_links(message.text) + extract_links(message.caption)
            if not urls:
                await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                await message.reply_text("⚠️ No valid URLs found!", quote=True)
                return

            for url in urls:
                if not await check_url_patterns_async(url):
                    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                    await message.reply_text("⚠️ Not a valid Terabox URL!", quote=True)
                    continue

                await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
                process_url = await message.reply_text("🔎 Processing URL...", quote=True)
                link_data = await fetch_download_link_async(url)

                # Ensure link_data is a list of dictionaries, each representing a download link
                if not isinstance(link_data, list):
                    raise Exception("Unexpected data format received from fetch_download_link_async")

                # Format messages for each link_data entry
                formatted_messages = await format_message(link_data)

                # Send formatted messages
                for formatted_message in formatted_messages:
                    await client.send_message(message.chat.id, formatted_message, parse_mode='html')

                end_time = time.time()
                time_taken = end_time - start_time
                download_message = (
                    f"🔗 <b>Links Bypassed!</b>\n\n<b>Time Taken</b>: {time_taken:.2f} seconds"
                )
                await process_url.edit_text(download_message)

        except Exception as e:
            await message.reply_text(f"Error: {e}", quote=True)


# run the application
app.run()
