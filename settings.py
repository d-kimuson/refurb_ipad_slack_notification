from chrome_handler import ChromeHandler
from slack import WebClient
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

# chrome handler config
chrome_driver_path = os.path.join(
    os.path.expanduser("~"),
    "Selenium",
    "chromedriver83"
)
handler = ChromeHandler(
    chrome_driver_path=chrome_driver_path, is_browser=True
)

# scraping config
base_url = "https://www.apple.com"
url_dict: Dict[str, Dict[str, str]] = {
    "64": {
        "silver": "/jp/shop/product/FTXP2J/A/",
        "gray": "/jp/shop/product/FTXN2J/A/",
    },
    "256": {
        "silver": "/jp/shop/product/FTXR2J/A/",
        "gray": "/jp/shop/product/FTXQ2J/A/",
        "test": "/jp/shop/product/FK9P2J/A/",
    },
}
wait_time = 30

# slack config
bot_token = os.environ.get("BOT_TOKEN")
slack_client = WebClient(token=bot_token)
