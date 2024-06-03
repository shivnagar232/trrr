import time
import logging
import asyncio
from pyrogram import Client, filters, enums
from config import session_string, allowed_groups, owner_id, extract_links
from downloader import check_url_patterns_async, fetch_download_link_async, get_formatted_size_async

API_ID = "19748984"  # Replace with your API_ID from config.py
API_HASH = "2141e30f96dfbd8c46fbb5ff4b197004"  # Replace with your API_HASH from config.py
BOT_TOKEN = "6399306217:AAFpGkkyZSOZoQJuMg5bR6AV4P-OmbFs1a4"  # Replace with your BOT_TOKEN from config.py

app = Client(
    name="ggn",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)

logging.basicConfig(level=logging.INFO)


@app.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type.value != "private" and str(message.chat.id) not in allowed_groups:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text("⚠️ Forbidden!\nFor groups access.\nContact @DTMK_C", quote=True)
        return
    else:
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await message.reply_text(
            "Hello! I am testing... being test by Team SPY, send Terabox link\n"
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

                if link_data:
                    for link in link_data:
                        file_name = link["server_filename"]
                        download_link = link["dlink"]
                        file_size = await get_formatted_size_async(link["size"])

                        # Download the file
                        async with client.download_media(download_link, file_name=file_name) as file_path:
                            # Upload the downloaded file
                            await client.send_document(message.chat.id, file_path, caption=f"🔗 <b>Fukkkked TeraBox!</b>\n\n"
                                                                                              f"┎ <b>Title</b>: `{file_name}`\n"
                                                                                              f"┠ <b>Size</b>: `{file_size}`\n"
                                                                                              f"┖ <b>Link</b>: <a href={download_link}>Link</a>\n\n"
                                                                                              f"Powered by __**Team SPY**__")

                download_message = f"🔗 <b>Mil gya pom pom enjoy!</b>\n\n<b>Time Taken</b>: {time_taken:.2f} seconds"
                await process_url.edit_text(download_message)

        except Exception as e:
            await message.reply_text(f"Error: {e}", quote=True)


# Run the application
app.run()
