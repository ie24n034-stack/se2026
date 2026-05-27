# ソフト名: Karen's Task Manager (CLI版)

## 機能
* 課題（タスク）の登録・編集・削除・一覧表示機能
* ステータス管理（未着手・進行中・完了）
* 締切が近いタスクの強調表示（リマインド機能）
* MariaDB を使用したデータの永続化

## 使い方
1. `python main.py list`：登録されている課題を一覧表示します。
2. `python main.py add`：新しい課題を対話形式で登録します。
3. `python main.py edit [ID]`：特定の課題の進捗や内容を更新します。
4. `python main.py delete [ID]`：不要になった課題を削除します。

## 作者
* 俵 佳蓮 (Karen Tawara)
