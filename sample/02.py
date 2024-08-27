import logging

# 親ロガーの作成
parent_logger = logging.getLogger('parent')
parent_logger.setLevel(logging.DEBUG)

# 子ロガーの作成
child_logger = logging.getLogger('parent.child')
child_logger.setLevel(logging.DEBUG)

# コンソールハンドラの作成と設定
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# ハンドラを親ロガーに追加
parent_logger.addHandler(console_handler)

# 子ロガーでログメッセージを生成
child_logger.debug('これは子ロガーのデバッグメッセージです')
child_logger.info('これは子ロガーの情報メッセージです')
