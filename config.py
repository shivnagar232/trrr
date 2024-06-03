import os
import logging
import re

logger = logging.getLogger(__name__)

# Define your cookie and headers directly as strings
my_cookie = '''__bid_n=18eaf16f59476e81ad4207;browserid=OOLSLjtNfKPkmhSgSK7lFioUS0lhp43Tp85a4L52TMLO4YZXX17IEe85M04=;TSID=ycjxBDKSB510s1P1rBcPJ2FQmfH2aO3x;__stripe_mid=ae1f9c32-b3c5-4dde-af48-3052794794ca187e65;_ga=GA1.1.1997931195.1712379212;g_state={"i_l":0};csrfToken=qxACy0Ws5byChVjWPocrk1te;lang=en;ndus=Y-PlW37teHuikdsetFXZFvHHhGL4yjIiVx-StRwU;ndut_fmt=2FF15F31454A89DCCCB7B65D77BAA74F6591C765B84E7324C48EE4B01FC50268;ab_sr=1.0.1_NTgxZjA2MTEyYTM4Y2ExM2RhMmRlODI3OThlMzBkMGNiODNkMWQ0ZDEwY2E3MDNlNGIwMzhlNmY2NWQ4Zjc3OGI4MThkMWE3MmUyNmEwODUyNmJkNmIyNDY0OGQ3MmUwN2Y4MTA2OTM1YjA4YjI4NmEyM2VhMDg1MzA0NmRkMDE0NTA3NTZkYzA4MjhhMThhYTFiY2Q4YzQ2NWZkYjljYQ==;ab_ymg_result={"data":"dccc7280ec7d0246f9f7c8c2013d1bb8ec63d9bcf8373cf401aa3d1b733c05978a6e4646bd9588d30fc4f69b813af5fb9376c7316a14cfbfcd251a8db1dc29f7ea727411bf7e2c01014b1375083d82b9e7560d199fac21700216c999d38125ea4992124a1984e0944e0daad59a98f9a8e238645c0162c013f5712bf9c74bf8af","key_id":"66","sign":"8868bc6b"};_ga_06ZNKL8C2E=GS1.1.1717424786.5.1.1717425277.60.0.0'''
my_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,hi-IN;q=0.8,hi;q=0.7",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Cookie": my_cookie,
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

# Define other variables as needed
session_string = "BQGUFZYAIcLZ8Gj0jmkiAHriyZ0m2veFedkze8TuOxyqWD149UJjqqBDJ6oWY-5jdfcfD-ze2D5mophOlp4LFbBYqjfJQvh_zxgPUzcfnerzSOfA1u_OcVUrPnml5xLdlavnucEPkWkiR9NBCl7pO2M1n03KBv0HfOHX4eNI2HjtypejWDx-OiTDqBHLY2xJAtjUxb01SxT58zg9zH--gPokXM3lfA-MaNms53ycjMjIIg3GtFFhhAM7ewQBMIdUm-D4mzf8vxEiqWhvd_Z4CmSrn1x7YR2tZ3GVjfyTg-Cqg4hZHJ_DpddYokjxtszvPC91YcibkggmxhceiRycV9UCciJuKAAAAAGSL3BcAA"
allowed_groups = "-123232ZCVZB"  # added random group id to avoid NoneType error
owner_id = "6747549788"

try:
    # No need to eval here, just use the variables as they are defined
    allowed_groups = set(allowed_groups)
except Exception as e:
    logger.error(f"Error parsing env variables: {e}")


def extract_links(message):
    # fetch all links
    try:
        url_pattern = r'https?://\S+'
        matches = re.findall(url_pattern, message)

        return matches
    except Exception as e:
        logger.error(f"Error extracting links: {e}")
        return []
