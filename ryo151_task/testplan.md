
# テストプラン（testplan.md）

## 1. テスト目的
本テストプランは、開発した「SportTrack CLI」が、要件定義に定められた必須機能（記録・表示・エラーハンドリング）を正しく満たしているかを検証する。

## 2. テスト項目一覧

| # | テスト項目 | 入力・操作 | 期待する結果 | 実際の結果 | 判定 |
|---|---|---|---|---|---|
| 1 | ヘルプ表示機能の検証 | `python main.py --help` を実行 | 利用可能なコマンド一覧（config, status, run等）の説明が標準出力に正しく表示されること | 実際の出力：<br>`config 初期設定を行い、保存領域を作ります`<br>`status これまでの全トレーニング履歴を表示します`<br>`run トレーニング記録を追加します` | 🟢 合格 |
| 2 | 初期設定機能の検証 | `python main.py config` を実行 | `~/.config/sport-track/` 内に `data.json` が新規生成され、完了メッセージが出ること | 実際の出力：<br>`【INFO】初期設定を開始します...`<br>`【SUCCESS】保存ファイルを作成しました: C:\Users\hr200/.config/sport-track\data.json` | 🟢 合格 |
| 3 | 筋トレの記録追加テスト | `python main.py run "ベンチプレス 60kg 10回"` を実行 | 「【SUCCESS】記録を追加しました」と表示され、JSONファイルに保存されること | 実際の出力：<br>`【SUCCESS】記録を追加しました: [2026-05-27 10:35:31] ベンチプレス 60kg 10回` | 🟢 合格 |
| 4 | ランニングの記録追加テスト | `python main.py run "ランニング 5km 25分"` を実行 | 同様に、既存のデータを消さずに2つ目の記録として正しく追記されること | 実際の出力：<br>`【SUCCESS】記録を追加しました: [2026-05-27 10:35:35] ランニング 5km 25分` | 🟢 合格 |
| 5 | 履歴の一覧表示テスト | `python main.py status` を実行 | 保存した筋トレとランニングの履歴が、日付とともに一覧で画面に表示されること | 実際の出力：<br>`=== hr200 のトレーニング履歴一覧 ===`<br>`📅 2026-05-27 10:35:31 ➔ ベンチプレス 60kg 10回`<br>`📅 2026-05-27 10:35:35 ➔ ランニング 5km 25分`<br>`=========================================` | 🟢 合格 |
| 6 | 不正なコマンドの入力（異常系） | `python main.py dance` を実行 | アプリがクラッシュせず、無効なコマンドである旨のメッセージが標準エラー出力に出ること | 実際の出力：<br>`main.py: error: argument command: invalid choice: 'dance' (choose from 'config', 'status', 'run')` | 🟢 合格 |
| 7 | 引数不足の入力（異常系） | `python main.py run` を実行 | 「記録する内容を入力してください」というエラーが出て安全に終了すること | 実際の出力：<br>`main.py: error: the following arguments are required: input` | 🟢 合格 |
| 8 | 応答速度の検証（非機能） | `powershell -Command "Measure-Command { python main.py status }"` を実行 | コマンドの処理（TotalSeconds）が 1秒以内 で完結すること | 実際の出力：<br>`TotalSeconds : 0.3870458`<br>（約0.38秒で処理が完了し、1秒以内の要件を満たした） | 🟢 合格 |
