import os
import logging
import re
import http.cookiejar  # Import the necessary module for cookies

logger = logging.getLogger(__name__)

# Define your cookies file path
COOKIES_FILE = 'cookies.txt'

# Initialize a MozillaCookieJar object
cookie_jar = http.cookiejar.MozillaCookieJar()

# Load cookies from the file
try:
    cookie_jar.load(COOKIES_FILE, ignore_discard=True, ignore_expires=True)
except Exception as e:
    logger.error(f"Failed to load cookies from {COOKIES_FILE}: {e}")

# Convert loaded cookies into a format usable by aiohttp
my_cookie = {cookie.name: cookie.value for cookie in cookie_jar}

my_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Dnt": "1",
    "Host": "www.terabox.com",
    "Origin": "https://www.terabox.com",
    "Referer": "https://www.terabox.com/main?category=all",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": "\"Android\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
}

session_string = "BQGUFZYAIcLZ8Gj0jmkiAHriyZ0m2veFedkze8TuOxyqWD149UJjqqBDJ6oWY-5jdfcfD-ze2D5mophOlp4LFbBYqjfJQvh_zxgPUzcfnerzSOfA1u_OcVUrPnml5xLdlavnucEPkWkiR9NBCl7pO2M1n03KBv0HfOHX4eNI2HjtypejWDx-OiTDqBHLY2xJAtjUxb01SxT58zg9zH--gPokXM3lfA-MaNms53ycjMjIIg3GtFFhhAM7ewQBMIdUm-D4mzf8vxEiqWhvd_Z4CmSrn1x7YR2tZ3GVjfyTg-Cqg4hZHJ_DpddYokjxtszvPC91YcibkggmxhceiRycV9UCciJuKAAAAAGSL3BcAA"
allowed_groups = "-123232ZCVZB"  # added random group id to avoid NoneType error
owner_id = "6747549788"

try:
    my_headers = eval(my_headers)
    allowed_groups = eval(allowed_groups)
except Exception as e:
    logger.error(f"Error parsing headers or allowed groups: {e}")


def extract_links(message):
    # fetch all links
    try:
        url_pattern = r'https?://\S+'
        matches = re.findall(url_pattern, message)

        return matches
    except Exception as e:
        logger.error(f"Error extracting links: {e}")
        return []
