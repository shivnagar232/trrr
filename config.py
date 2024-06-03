import os
import logging
import re

logger = logging.getLogger(__name__)

my_cookie = '''browserid=3GfguDDKfz5xNSE04XnM-Ef9K_5ghRugLiDUNmIng8UHpKPE-9PFsxS9mGA=;TSID=taEbjzmvRpn56N5ftlIAr4acTpcj7qUf;__bid_n=18eb1b8b92db6ee73a4207;g_state={"i_l":0};ndus=Y-PlW37teHuifl29AQxXZ-7M7GNm_yRZiBuzKU5k;ab_jid=c7c6332012c604797bbec4532b418c1d52bf;csrfToken=uZ_NrouxNEMIzL5Jd3IrjgLy;lang=en;ndut_fmt=4220686A9795E68F7B8C11A496500A7677B9B69D284C8E8429F8A89843E9E855;ab_bid=804745b29f924583f8fb3e43d2aac10b9cd1;ab_sr=1.0.1_MmZiMWU4OGZjNTdhYjIwOTA1YjY4YTkyM2QwMmZmNDI1M2VhNzIwYmFiNDg4YmI2OGVkODIyY2I4ZmY0NThkNGU2MWEwYTVjOTU5MWQ1MDZjYTcxZmI2Zjc4ZWI5N2NmOTUyNmUwOGU4MjFlMTZhODE3NWIzYjYzMTg3ZmRmZjg3YWI3ZmE3MmZhMzYwNGY1NmQ1OTM5YmU1ZmVhMTg0OA==;ab_ymg_result={"data":"dccc7280ec7d0246f9f7c8c2013d1bb8ec63d9bcf8373cf401aa3d1b733c0597171ef8359c1f5ac7526a62c82fc38d920380833b06c1efb82df13ab95168c99825a21311cc4984a952d234eca56e48a1805a15d3fc0b96dd80946b39e423af8528c32fad0701e5d6ac237772f8227b3d24ac71e9c8b1fa53be0cc1ef63755b6e","key_id":"66","sign":"21878b1e"};_ga=GA1.1.1659176144.1717420695;_ga_06ZNKL8C2E=GS1.1.1717420695.1.0.1717420723.32.0.0'''

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

session_string = "BQGUFZYAIcLZ8Gj0jmkiAHriyZ0m2veFedkze8TuOxyqWD149UJjqqBDJ6oWY-5jdfcfD-ze2D5mophOlp4LFbBYqjfJQvh_zxgPUzcfnerzSOfA1u_OcVUrPnml5xLdlavnucEPkWkiR9NBCl7pO2M1n03KBv0HfOHX4eNI2HjtypejWDx-OiTDqBHLY2xJAtjUxb01SxT58zg9zH--gPokXM3lfA-MaNms53ycjMjIIg3GtFFhhAM7ewQBMIdUm-D4mzf8vxEiqWhvd_Z4CmSrn1x7YR2tZ3GVjfyTg-Cqg4hZHJ_DpddYokjxtszvPC91YcibkggmxhceiRycV9UCciJuKAAAAAGSL3BcAA"
allowed_groups = "-123232ZCVZB"  # added random group id to avoid NoneType error
owner_id = "6747549788"

try:
    allowed_groups = eval(allowed_groups)
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
