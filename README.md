# logging について

## ロガー

### 役割

- ログメッセージの生成、管理を行うオブジェクト
- ログメッセージを受け取り、指定された出力先へ出力する

### 概要

- 階層構造で表現する
- 子ロガーのログが親(root)ロガーへ伝播する(参考: 02.py)
  - 親がdebugレベル、子がerrorレベルの場合にinfoのログが出力された場合の例
    1. 子はerrorなので、infoレベルは無視して出力しない
    2. 次に親に伝播
    3. 親は、debugレベルなので、infoレベルを出力する
    4. 結果infoレベルのログが出力される(rootロガーによって出力される)
- ロガーの名前は、__name__ の値を入れるのがベストプラクティス
    <pre>logger = logging.getLogger(__name__)</pre>


## ハンドラー

### 役割

- ログメッセージの出力先や挙動を制御するためのコンポーネント

### 概要

- 複数のハンドラーを一つのロガーに追加可能
- 異なる出力先に同時にログを送ることを可能にする
- 一定の時間間隔でログファイルをローテーション可能
    <pre>timed_handler = TimedRotatingFileHandler('app.log', when='midnight', interval=1)</pre>
- ログメッセージをメール送信(例: 03.py)
- ログメッセージをHTTPリクエストとして送信(例: 04.py)
- 出力先指定
  - 標準出力
    <pre>stream_handler = logging.StreamHandler()</pre>
  - ファイル
　　<pre>file_handler = logging.FileHandler('app.log')</pre>
- ファイル出力(ローテーションあり)の例
  <pre>
  import logging
  from logging.handlers import RotatingFileHandler

  rotating_handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5)
  logger.addHandler(rotating_handler)
  </pre>

### 設定

- ログレベルやフォーマッタを設定可能(例: 05.py)

## サンプル

```python
import logging

# -----------------------------------------------
# 1. ロガーを取得
# -----------------------------------------------
logger = logging.getLogger(__name__)

# ルートロガーの設定
logging.basicConfig(level=logging.DEBUG)

# -----------------------------------------------
# 2. ハンドラを設定
# -----------------------------------------------
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)  # ハンドラーのログレベルを設定

file_handler = logging.FileHandler('file_handler_output_test.txt')
file_handler.setLevel(logging.INFO)  # ハンドラーのログレベルを設定

# フォーマットの定義
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# フォーマッタを設定(標準出力)
stream_handler.setFormatter(formatter)

# フォーマッタを設定(ファイル出力)
file_handler.setFormatter(formatter)

# -----------------------------------------------
# 3. 作成したハンドラをロガーに追加する
# -----------------------------------------------
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# -----------------------------------------------
# 4. ログを出力
# -----------------------------------------------
logger.debug('デバッグメッセージ')
logger.info('情報メッセージ')
logger.warning('警告メッセージ')
logger.error('エラーメッセージ')
logger.critical('重大なエラーメッセージ')
