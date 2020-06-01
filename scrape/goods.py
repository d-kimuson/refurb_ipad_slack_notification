from traceback import format_exc
from time import sleep
from pprint import pprint
from typing import List

from settings import handler, base_url, slack_client, wait_time


class Good:
    """整備品

    スクレイピングによって取得した在庫情報を保持するクラス

    Attributes:
        title {str} -- 商品名
        url {str} -- 購入ページへのリンク
    """

    def __init__(self, identifier: str, title: str, url: str) -> None:
        self.identifier = identifier
        self.title = title.replace("[整備済製品]", "")
        self.url = url

    def __hash__(self) -> int:
        return self.identifier.__hash__()

    def __eq__(self, other: 'Good') -> bool:
        return self.__hash__() == other.__hash__()

    def __repr__(self) -> str:
        return "{}".format(self.title)

    __str__ = __repr__

    def send_slack(self) -> None:
        slack_client.chat_postMessage(
            channel='apple整備品通知',
            text='{} の整備品が追加されたよ！ => {}'.format(
                self.title,
                self.url
            )
        )


def run() -> None:
    """メインタスクの実行関数
    """
    history = scrape_good_list()

    try:
        while True:
            try:
                print("# 整備品一覧の取得")
                current = scrape_good_list()
                print("# 一覧取得の終了. 前回の一覧と比較します.")
                added_list = get_added_good_list(before=history, after=current)
                print("追加一覧: ", end='')
                pprint(added_list)
                for item in added_list:
                    item.send_slack()
            except Exception as e:
                print(e, type(e))
                format_exc()
            finally:
                print(f"# 一覧取得の終了. 待機時間({wait_time})に入ります.\n\n")

            sleep(wait_time)
    except Exception as e:
        print(e, type(e))
    finally:
        handler.fin()


def scrape_good_list() -> List[Good]:
    """Apple公式サイトから整備品の在庫一覧を取得する関数

    Args:
        handler (ChromeHandler): スクレイピング用のハンドラ

    Returns:
        List[Good]: 在庫一覧
    """
    handler.access(
        base_url + "/jp/shop/refurbished/ipad", cl="as-gridpage-producttiles"
    )

    handler.set_soup()
    items = handler.soup.find(class_="as-gridpage-producttiles").find_all("li")

    results: List[Good] = []
    for item in items:
        link_to_item = item.find(class_="as-producttile-info").h3.a

        title = link_to_item.get("data-display-name")
        identifier = link_to_item.get("data-part-number")
        url = link_to_item.get("href")
        formatted_url = base_url + url.replace(url.split("/")[-1], "")

        results.append(Good(identifier, title, formatted_url))

    return results


def get_added_good_list(before: List[Good], after: List[Good]) -> List[Good]:
    """在庫一覧の履歴(前後)から, 追加された整備品の一覧を返す関数

    Args:
        before (List[Good]): 前回の整備品一覧
        after (List[Good]): 今回の整備品一覧

    Returns:
        List[Good]: 追加された整備品の一覧
    """
    return list(
        set(after) - set(before)
    )
