import logging

# -----------------------------------------------
# フィルター（Filter）のサンプル
#
# フィルターを使うと、ログレベル以外の条件で
# ログの出力を制御できる。
#
# ロガー・ハンドラーの両方に追加可能。
# -----------------------------------------------


# -----------------------------------------------
# 1. カスタムフィルターを定義
# -----------------------------------------------

class ExactLevelFilter(logging.Filter):
    """指定したレベルのログだけを通過させるフィルター"""

    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        # record.levelno が指定レベルと一致する場合のみ True を返す
        return record.levelno == self.level


class KeywordFilter(logging.Filter):
    """メッセージに特定のキーワードを含むログだけを通過させるフィルター"""

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def filter(self, record):
        return self.keyword in record.getMessage()


# -----------------------------------------------
# 2. ロガーを取得
# -----------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# -----------------------------------------------
# 3. ハンドラーを作成してフィルターを追加
# -----------------------------------------------

# WARNING レベルのみを標準出力へ出力するハンドラー
warning_only_handler = logging.StreamHandler()
warning_only_handler.setLevel(logging.DEBUG)  # フィルターで制御するので DEBUG に設定
warning_only_handler.addFilter(ExactLevelFilter(logging.WARNING))

# "重要" というキーワードを含むログのみをファイルへ出力するハンドラー
keyword_handler = logging.FileHandler('filter_output_test.txt')
keyword_handler.setLevel(logging.DEBUG)
keyword_handler.addFilter(KeywordFilter('重要'))

# フォーマッタを設定
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
warning_only_handler.setFormatter(formatter)
keyword_handler.setFormatter(formatter)

# -----------------------------------------------
# 4. ハンドラーをロガーに追加
# -----------------------------------------------
logger.addHandler(warning_only_handler)
logger.addHandler(keyword_handler)

# -----------------------------------------------
# 5. ログを出力して動作を確認
# -----------------------------------------------

# warning_only_handler → WARNING のみ出力
# keyword_handler      → "重要" を含むものだけ出力
logger.debug('デバッグメッセージ')           # どちらにも出力されない
logger.info('情報メッセージ（重要）')        # keyword_handler のみ出力
logger.warning('警告メッセージ')            # warning_only_handler のみ出力
logger.warning('重要な警告メッセージ')      # 両方のハンドラーに出力
logger.error('エラーメッセージ（重要）')    # keyword_handler のみ出力
logger.critical('重大なエラーメッセージ')   # どちらにも出力されない
