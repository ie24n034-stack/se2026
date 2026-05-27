# Design Document

## アーキテクチャ
- **Entry Point**: `main.go` (または `index.ts` 等) が引数を解析
- **Command Layer**: 各コマンド（Add, List, Delete等）のロジックを分離
- **Config Loader**: ユーザー設定の永続化
- **Internal Lib**: コアとなるビジネスロジック

## インターフェース案
- `app config`: 初期設定
- `app exec [target]`: メイン処理の実行
- `app status`: 現在の状態確認

## データ保存
- ローカルの `~/.config/[app-name]/` 内に保存
