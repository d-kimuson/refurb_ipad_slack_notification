from chrome_handler import ChromeHandler
from slack import WebClient
from time import sleep
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

chrome_driver_path = os.path.join(
    os.path.expanduser('~'), 'Selenium', 'chromedriver83'
)
base_url = 'https://www.apple.com'
bot_token = os.environ.get('BOT_TOKEN')
slack_client = WebClient(token=bot_token)

url_dict = {
    '64': {
        'silver': 'https://www.apple.com/jp/shop/product/FTXP2J/A/',
        'gray': 'https://www.apple.com/jp/shop/product/FTXN2J/A/'
    },
    '256': {
        'silver': 'https://www.apple.com/jp/shop/product/FTXR2J/A/',
        'gray': 'https://www.apple.com/jp/shop/product/FTXQ2J/A/',
        'test': 'https://www.apple.com/jp/shop/product/FK9P2J/A/'
    }
}


def scrape(handler: ChromeHandler) -> List[Dict[str, str]]:
    handler.access(base_url + '/jp/shop/refurbished/ipad', cl='as-gridpage-producttiles')
    handler.set_soup()
    items = handler.soup.find(class_='as-gridpage-producttiles').find_all('li')

    results: List[Dict[str, str]] = []
    for item in items:
        link_to_item = item.find(class_='as-producttile-info').h3.a
        title = link_to_item.get('data-display-name')
        url = link_to_item.get('href')
        formatted_url = base_url + url.replace(url.split('/')[-1], '')

        print(title, formatted_url)
        results.append({
            'title': title,
            'url': formatted_url
        })
    
    return results


if __name__ == '__main__':
    handler = ChromeHandler(chrome_driver_path=chrome_driver_path, is_browser=False)
    try:
        history = scrape(handler)

        while(True):
            print("# チェック開始")
            items = scrape(handler)
            sleep(5)
            print("# チェック終了\n")

            if len(history) < len(items):
                # 追加判定
                diffs = list(set(items) - set(history))
                if len(diffs) != 0:
                    print("追加一覧(今回 - 前回)")
                    for item in diffs:
                        print(item['title'], ' => ', item['url'])
                        slack_client.chat_postMessage(
                            channel='apple整備品通知',
                            text='{} の整備品が追加されたよ！ => {}'.format(item['title'], item['url'])
                        )
                    
                    print("\n")
            
            history = items
            sleep(30)  # 30秒ごとに確認
    except Exception as e:
        print(e)
    finally:
        handler.fin()

