# Python `logging` モジュール 学習仕様書

## 概要

本ワークスペースは、Python 標準ライブラリの `logging` モジュールの使い方を体系的に学ぶためのサンプル集です。  
ロガー・ハンドラー・フォーマッタ・フィルターの基本概念から、メール送信・HTTP送信などの応用ハンドラーまでを段階的に習得することを目的としています。

---

## ディレクトリ構成

```
python_logging/
├── README.md                       # 学習ノート（概念整理）
├── file_handler_output_test.txt    # FileHandler の出力先ファイル
├── filter_output_test.txt          # Filter サンプルの出力先ファイル
├── docs/
│   └── spec.md                     # 本仕様書
└── sample/
    ├── 01.py   # 基本構成（StreamHandler + Formatter）
    ├── 02.py   # ロガーの階層構造と伝播
    ├── 03.py   # SMTPHandler（メール送信）
    ├── 04.py   # HTTPHandler（HTTP送信）
    ├── 05.py   # 複数ハンドラーの組み合わせ（StreamHandler + FileHandler）
    └── 06.py   # フィルター（カスタム Filter の定義と適用）
```

---

## コンポーネント仕様

### 1. ロガー（Logger）

| 項目 | 内容 |
|------|------|
| 役割 | ログメッセージの生成・管理を行うオブジェクト |
| 取得方法 | `logging.getLogger(__name__)` |
| 階層構造 | `.` 区切りの名前で親子関係を表現（例: `parent` / `parent.child`） |
| ログ伝播 | 子ロガーのログは親ロガーへ自動伝播する（`propagate=True` がデフォルト） |
| ベストプラクティス | `logger = logging.getLogger(__name__)` でモジュール名をロガー名に使用 |

#### ログレベル一覧

| レベル | 定数値 | 用途 |
|--------|--------|------|
| DEBUG | 10 | 詳細なデバッグ情報 |
| INFO | 20 | 正常動作の確認 |
| WARNING | 30 | 予期しない事象（デフォルトレベル） |
| ERROR | 40 | 機能が実行できないエラー |
| CRITICAL | 50 | 重大なエラー |

#### 伝播の動作例（02.py より）

```
親ロガー: DEBUG レベル
子ロガー: ERROR レベル
→ 子ロガーに INFO を渡した場合

1. 子ロガーは ERROR レベルなので INFO を無視（出力しない）
2. 親ロガーへ伝播
3. 親ロガーは DEBUG レベルなので INFO を処理
4. 結果: INFO ログが親ロガー（ルートロガー）によって出力される
```

---

### 2. ハンドラー（Handler）

| 項目 | 内容 |
|------|------|
| 役割 | ログメッセージの出力先・挙動を制御するコンポーネント |
| 複数追加 | 1つのロガーに複数ハンドラーを追加可能 |
| レベル設定 | ハンドラーごとに独立したログレベルを設定可能 |

#### ハンドラー種別

| ハンドラー | インポート元 | 出力先 | 使用例 |
|-----------|------------|--------|--------|
| `StreamHandler` | `logging` | 標準出力（コンソール） | 01.py, 02.py, 05.py |
| `FileHandler` | `logging` | ファイル | 05.py |
| `RotatingFileHandler` | `logging.handlers` | ファイル（サイズでローテーション） | README.md |
| `TimedRotatingFileHandler` | `logging.handlers` | ファイル（時間でローテーション） | README.md |
| `SMTPHandler` | `logging.handlers` | メール送信 | 03.py |
| `HTTPHandler` | `logging.handlers` | HTTP リクエスト送信 | 04.py |

#### RotatingFileHandler の設定例

```python
from logging.handlers import RotatingFileHandler
rotating_handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5)
logger.addHandler(rotating_handler)
```

#### TimedRotatingFileHandler の設定例

```python
from logging.handlers import TimedRotatingFileHandler
timed_handler = TimedRotatingFileHandler('app.log', when='midnight', interval=1)
```

---

### 3. フォーマッタ（Formatter）

| 属性 | 意味 |
|------|------|
| `%(asctime)s` | ログ出力日時 |
| `%(name)s` | ロガー名 |
| `%(levelname)s` | ログレベル名 |
| `%(message)s` | ログメッセージ本文 |

標準フォーマット例:
```python
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```

---

### 4. フィルター（Filter）

| 項目 | 内容 |
|------|------|
| 役割 | ログレベル以外の条件でログの通過・遮断を制御するコンポーネント |
| 追加対象 | ロガー・ハンドラーの両方に追加可能 |
| 定義方法 | `logging.Filter` を継承し、`filter(record)` メソッドをオーバーライドする |
| 戻り値 | `True` でログを通過、`False` で遮断 |

#### カスタムフィルターの基本構造

```python
class MyFilter(logging.Filter):
    def filter(self, record):
        # True を返すとログが通過、False で遮断
        return 条件式
```

#### `LogRecord` の主な属性

| 属性 | 内容 |
|------|------|
| `record.levelno` | ログレベルの数値（例: `logging.WARNING` = 30） |
| `record.name` | ロガー名 |
| `record.getMessage()` | ログメッセージ文字列 |
| `record.filename` | ログが発生したファイル名 |
| `record.funcName` | ログが発生した関数名 |

---

## サンプルファイル仕様

### 01.py — 基本構成

**目的:** ロガー・ハンドラー・フォーマッタの最小構成を学ぶ

| 項目 | 設定値 |
|------|--------|
| ロガー | `__name__` |
| ハンドラー | `StreamHandler`（標準出力） |
| フォーマッタ | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` |

**動作:** DEBUG / INFO / WARNING / ERROR / CRITICAL の5レベルをコンソールへ出力

---

### 02.py — ロガーの階層構造と伝播

**目的:** 親子ロガーの関係とログ伝播の動作を理解する

| ロガー | 名前 | レベル |
|--------|------|--------|
| 親 | `parent` | DEBUG |
| 子 | `parent.child` | DEBUG |

**ハンドラー:** `StreamHandler` を親ロガーのみに追加  
**動作:** 子ロガーのメッセージが親ロガーを通じてコンソールへ出力される

---

### 03.py — SMTPHandler（メール送信）

**目的:** ログをメールで通知する方法を示す

| 項目 | 設定値 |
|------|--------|
| SMTPサーバー | `smtp.example.com:587` |
| 送信元 | `from@example.com` |
| 送信先 | `to@example.com` |
| 件名 | `Application Error` |

> **注意:** 動作確認には実際の SMTP サーバー情報への差し替えが必要

---

### 04.py — HTTPHandler（HTTP送信）

**目的:** ログを HTTP リクエストとして外部サービスへ送信する方法を示す

| 項目 | 設定値 |
|------|--------|
| ホスト | `www.example.com` |
| エンドポイント | `/log` |
| メソッド | `POST` |

> **注意:** 動作確認には実際のエンドポイントへの差し替えが必要

---

### 05.py — 複数ハンドラーの組み合わせ

**目的:** 複数のハンドラーを同一ロガーに設定し、出力先とレベルを個別に制御する

| ハンドラー | 出力先 | ログレベル |
|-----------|--------|-----------|
| `StreamHandler` | 標準出力 | WARNING 以上 |
| `FileHandler` | `file_handler_output_test.txt` | INFO 以上 |

**動作:**
- `logger.debug(...)` → どこにも出力されない
- `logger.info(...)` → ファイルのみ出力
- `logger.warning(...)` → コンソール + ファイルの両方に出力

---

### 06.py — フィルター（Filter）

**目的:** カスタムフィルターを定義し、ログレベル以外の条件で出力を制御する

#### 定義するフィルター

| フィルター | 条件 |
|-----------|------|
| `ExactLevelFilter` | 指定したレベルと完全一致するログのみ通過 |
| `KeywordFilter` | メッセージに指定キーワードを含むログのみ通過 |

#### ハンドラーとフィルターの対応

| ハンドラー | 出力先 | 適用フィルター | 通過条件 |
|-----------|--------|--------------|---------|
| `StreamHandler` | 標準出力 | `ExactLevelFilter(WARNING)` | WARNING レベルのみ |
| `FileHandler` | `filter_output_test.txt` | `KeywordFilter('重要')` | "重要" を含むメッセージのみ |

#### 各ログメッセージの出力先

| メッセージ | コンソール | ファイル |
|-----------|-----------|---------|
| `debug('デバッグメッセージ')` | ✗ | ✗ |
| `info('情報メッセージ（重要）')` | ✗ | ✓ |
| `warning('警告メッセージ')` | ✓ | ✗ |
| `warning('重要な警告メッセージ')` | ✓ | ✓ |
| `error('エラーメッセージ（重要）')` | ✗ | ✓ |
| `critical('重大なエラーメッセージ')` | ✗ | ✗ |

---

## 学習の進め方（推奨順）

1. **01.py** — 基本的な構成を把握する
2. **02.py** — 階層構造と伝播の挙動を確認する
3. **05.py** — 複数ハンドラーでの出力制御を理解する
4. **06.py** — フィルターによるきめ細かな制御を学ぶ
5. **03.py / 04.py** — 応用ハンドラーの概念を把握する
6. **README.md** — RotatingFileHandler / TimedRotatingFileHandler を確認する
