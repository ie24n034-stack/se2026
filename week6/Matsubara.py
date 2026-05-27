import argparse
import csv
import os
import sys
import time

# データ保存用のCSVファイル名
TASK_FILE = "tasks.csv"
HISTORY_FILE = "history.csv"


# 初期化: CSVファイルが存在しない場合はヘッダーを作成
def init_storage():
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Priority", "Status"])

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Duration_Sec"])


# 1. 認証コマンド（ダミー）
def handle_login(args):
    print(f"🔑 ユーザー '{args.username}' としてログインしました。")


# 2. タスク追加機能（Issue 3: CSV保存）
def handle_task_add(args):
    init_storage()
    # 既存のタスク数を数えて新しいIDを決める
    with open(TASK_FILE, "r", encoding="utf-8") as f:
        next_id = sum(1 for _ in f)

    with open(TASK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([next_id, args.title, args.priority, "未完了"])

    print(f"✅ タスクを追加しました: [{next_id}] {args.title} (優先度: {args.priority})")


# 3. タスク一覧表示機能（Issue 2: テーブル形式表示）
def handle_task_list(args):
    init_storage()
    print("\n" + "=" * 50)
    print(f"{'ID':<5} | {'タスク名':<20} | {'優先度':<6} | {'ステータス':<10}")
    print("-" * 50)

    with open(TASK_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # ヘッダーをスキップ
        for row in reader:
            print(f"{row[0]:<5} | {row[1]:<20} | {row[2]:<8} | {row[3]:<10}")
    print("=" * 50 + "\n")


# 4. タイマー機能（Issue 1: ビープ音 ＆ Issue 3: 履歴CSV保存）
def handle_timer_start(args):
    init_storage()
    # テスト用に引数から時間を指定可能（デフォルトは25分 = 1500秒）
    duration = args.seconds
    print(f"⏱  ポモドーロタイマーを開始します（{duration}秒間集中してください）...")

    try:
        for i in range(duration, 0, -1):
            # ターミナル上で上書きカウントダウン表示
            sys.stdout.write(f"\r残り時間: {i // 60:02d}:{i % 60:02d} ")
            sys.stdout.flush()
            time.sleep(1)

        print("\n\n🎉 タイムアップ！ お疲れ様でした！")

        # Issue 1: アラート音（ビープ音）を鳴らす
        sys.stdout.write("\a")
        sys.stdout.flush()

        # Issue 3: 学習履歴をCSVに保存
        today = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([today, duration])
        print(f"📊 学習履歴に {duration} 秒の記録を保存しました。")

    except KeyboardInterrupt:
        print("\n⏹ タイマーが中断されました。")


def main():
    parser = argparse.ArgumentParser(
        description="StudyTerm-CLI: ターミナル学習管理ツール"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # auth コマンド
    auth_parser = subparsers.add_parser("auth", help="ユーザー認証関連")
    auth_parser.add_argument("action", choices=["login"])
    auth_parser.add_argument("--username", default="matsubara")

    # task コマンド
    task_parser = subparsers.add_parser("task", help="タスク管理関連")
    task_sub = task_parser.add_subparsers(dest="action", required=True)

    task_add = task_sub.add_parser("add", help="タスクの追加")
    task_add.add_argument("title", help="タスクのタイトル")
    task_add.add_argument(
        "--priority", choices=["高", "中", "低"], default="中", help="優先度"
    )

    task_sub.add_parser("list", help="タスクの一覧表示")

    # timer コマンド
    timer_parser = subparsers.add_parser("timer", help="タイマー関連")
    timer_parser.add_argument("action", choices=["start"])
    timer_parser.add_argument(
        "--seconds", type=int, default=1500, help="タイマーの時間（秒）"
    )

    args = parser.parse_args()

    # コマンドの分岐処理
    if args.command == "auth" and args.action == "login":
        handle_login(args)
    elif args.command == "task" and args.action == "add":
        handle_task_add(args)
    elif args.command == "task" and args.action == "list":
        handle_task_list(args)
    elif args.command == "timer" and args.action == "start":
        handle_timer_start(args)


if __name__ == "__main__":
    main()
