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

