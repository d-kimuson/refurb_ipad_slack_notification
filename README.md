# Apple整備品 Slack通知アプリ

## 環境構築

### パッケージの取得

``` sh
$ pip install -r requirements.txt
```

### 環境ファイルの準備

`.env` ファイルを `.env.sample` を参考に, 置く.

``` txt
BOT_TOKEN=hogehoge
```

### chrome driver の設置

OSのChromeと同バージョンの `chromedriver` をダウンロードし, パスを `settings.py` の `chrome_driver_path` に記述.

## メインスレッドの起動

``` sh
$ python main.py
```
