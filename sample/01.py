import logging

# ロガーを取得
logger = logging.getLogger(__name__)

# ハンドラを設定
handler = logging.StreamHandler()

# フォーマッタを設定
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# ロガーにハンドラを追加
logger.addHandler(handler)

# ログを出力
logger.debug('デバッグメッセージ')
logger.info('情報メッセージ')
logger.warning('警告メッセージ')
logger.error('エラーメッセージ')
logger.critical('重大なエラーメッセージ')
