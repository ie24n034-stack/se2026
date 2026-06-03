# 設計書 (design.md)

## 1. アーキテクチャ構成
本ツールは保守性と「自分が説明できること」を重視し、以下の4つのレイヤー・役割に分解して実装する。

* **Entry Point (`main.py`)**: ユーザーからのコマンドライン引数（`sys.argv` / `argparse`）を解析し、各処理へ振り分ける窓口。
* **Command Layer**: `config`, `run`, `status` の各コマンドに対応する関数ロジック。
* **Data Storage (JSON)**: データベースの代わりに、軽量なJSONファイルを使ってデータを永続化する。

## 2. インターフェース仕様
* `python main.py config` : `~/.config/sport-track/` フォルダおよび初期ファイルを生成。
* `python main.py run "[テキスト]"` : 入力された文字列を履歴データに追加。
* `python main.py status` : 蓄積された履歴データを読み込んで一覧表示。

## 3. データ保存設計
ローカルマシンの以下のパスにJSON形式で永続化する。

* **保存先ディレクトリ**: `~/.config/sport-track/`
* **保存ファイル名**: `data.json`

### データ構造案 (JSON):
```json
{
  "user": "hr200",
  "created_at": "2026-05-27",
  "history": [
    {
      "date": "2026-05-27 10:15:30",
      "content": "ベンチプレス 60kg 10回"
    },
    {
      "date": "2026-05-27 10:16:00",
      "content": "ランニング 5km 25分"
    }
  ]
}
