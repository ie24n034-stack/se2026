import argparse
import json
import os
import time
import hashlib
from datetime import datetime

# データ設計に基づき、ローカルのJSONファイルにデータを保存します
DATA_FILE = "storage.json"

# --- 時間を「〇分〇秒」に変換するヘルパー関数 ---
def format_time(seconds):
    """秒数を「〇分〇秒」の形式に変換する"""
    minutes = seconds // 60
    rem_seconds = seconds % 60
    if minutes > 0:
        return f"{minutes}分{rem_seconds}秒"
    return f"{rem_seconds}秒"

def parse_time_arg(time_str):
    """'25m' や '45s' のような文字列を秒数(int)に変換する"""
    time_str = time_str.strip().lower()
    try:
        if time_str.endswith('m'):
            # 分指定の場合 (例: 3m -> 3 * 60 = 180秒)
            return int(time_str[:-1]) * 60
        elif time_str.endswith('s'):
            # 秒指定の場合 (例: 45s -> 45秒)
            return int(time_str[:-1])
        else:
            # 単位がない場合は秒数として扱う
            return int(time_str)
    except ValueError:
        print("警告: 時間の指定形式が正しくありません。デフォルトの15秒で開始します。 (例: 25m や 45s)")
        return 15

# --- 1. データ管理用の関数（データストレージ設計） ---
def load_data():
    """JSONファイルからデータを読み込む（ファイルがない場合は初期構造を返す）"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}, "tasks": [], "records": [], "current_user": None}

def save_data(data):
    """データをJSONファイルに書き込む"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_password(password):
    """セキュリティ要件：パスワードをSHA-256でハッシュ化（平文保存の禁止）"""
    return hashlib.sha256(password.encode()).hexdigest()


# --- 2. 各コマンドの処理（ロジック設計） ---
def cmd_register(args):
    """新規ユーザー登録 (register)"""
    data = load_data()
    username = input("希望するユーザー名を入力してください: ")
    if username in data["users"]:
        print("エラー: そのユーザー名は既に存在します。")
        return
    password = input("パスワードを入力してください: ")
    
    data["users"][username] = {
        "password": hash_password(password),
        "token": None
    }
    save_data(data)
    print(f"ユーザー '{username}' の登録が完了しました。")

def cmd_login(args):
    """ログイン (login)"""
    data = load_data()
    username = input("ユーザー名: ")
    password = input("パスワード: ")
    
    if username in data["users"] and data["users"][username]["password"] == hash_password(password):
        token = hashlib.md5(str(time.time()).encode()).hexdigest()
        data["users"][username]["token"] = token
        data["current_user"] = username
        save_data(data)
        print(f"ログイン成功！ こんにちは、{username}さん。")
    else:
        print("エラー: ユーザー名またはパスワードが正しくありません。")

def cmd_add(args):
    """学習タスク追加 (add)"""
    data = load_data()
    if not data["current_user"]:
        print("エラー: タスクを追加するには先にログインしてください。")
        return
    
    task_id = len(data["tasks"]) + 1
    new_task = {
        "task_id": task_id,
        "title": args.title,
        "deadline": "2026-06-30", 
        "priority": args.priority,
        "completed": False,
        "user": data["current_user"]
    }
    data["tasks"].append(new_task)
    save_data(data)
    print(f"タスクを追加しました: [ID: {task_id}] {args.title} (優先度: {args.priority})")

def cmd_list(args):
    """未完了タスク一覧表示 (list / ls)"""
    data = load_data()
    if not data["current_user"]:
        print("エラー: ログインしてください。")
        return
    
    user_tasks = [t for t in data["tasks"] if t["user"] == data["current_user"] and not t["completed"]]
    
    if not user_tasks:
        print("未完了のタスクはありません。")
        return
    
    print(f"{'ID':<4} | {'タスクタイトル':<25} | {'優先度':<6}")
    print("-" * 45)
    for t in user_tasks:
        print(f"{t['task_id']:<4} | {t['title']:<25} | {t['priority']:<6}")

def cmd_done(args):
    """タスク完了マーク (done)"""
    data = load_data()
    for t in data["tasks"]:
        if t["task_id"] == args.id and t["user"] == data["current_user"]:
            t["completed"] = True
            save_data(data)
            print(f"タスク ID {args.id} を完了にしました！")
            return
    print("エラー: 指定されたタスクが見つかりません。")

def cmd_delete(args):
    """タスク削除 (delete)"""
    data = load_data()
    if not data["current_user"]:
        print("エラー: ログインしてください。")
        return
    
    original_count = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if not (t["task_id"] == args.id and t["user"] == data["current_user"])]
    
    if len(data["tasks"]) < original_count:
        save_data(data)
        print(f"タスク ID {args.id} を削除しました。")
    else:
        print("エラー: 指定されたタスクが見つかりません。")

def cmd_start(args):
    """学習タイマー機能（自由な時間指定・一時停止・再開・分秒表示に対応）"""
    data = load_data()
    if not data["current_user"]:
        print("エラー: ログインしてください。")
        return
    
    # 入力された時間（25m や 45s など）を秒数に変換
    duration = parse_time_arg(args.time)
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"ポモドーロタイマーを開始します ({format_time(duration)})...")
    print("※ カウントダウン中に [Ctrl + C] を押すと一時停止（timer stop）できます。")
    
    remaining = duration
    try:
        while remaining > 0:
            print(f"\r残り時間: {format_time(remaining)}    ", end="", flush=True)
            time.sleep(1)
            remaining -= 1
            
    except KeyboardInterrupt:
        # 一時停止(timer stop)の処理
        print("\n\n--- タイマー一時停止 (timer stop) ---")
        choice = input("再開しますか？ (y: 再開(timer restart) / n: 中断して終了): ").strip().lower()
        if choice == 'y':
            print("タイマーを再開します (timer restart)...")
            try:
                while remaining > 0:
                    print(f"\r残り時間: {format_time(remaining)}    ", end="", flush=True)
                    time.sleep(1)
                    remaining -= 1
            except KeyboardInterrupt:
                print("\nタイマーが完全に中断されました。")
                return
        else:
            print("タイマーを終了しました。")
            return

    # タイマー正常終了
    print("\n\a時間です！休憩に入りましょう。")
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    record_id = len(data["records"]) + 1
    new_record = {
        "record_id": record_id,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": duration,
        "task_id": args.task_id,
        "user": data["current_user"]
    }
    data["records"].append(new_record)
    save_data(data)
    print("学習記録をデータストレージに保存しました。")

def cmd_summary(args):
    """学習履歴・進捗確認機能 (summary)"""
    data = load_data()
    if not data["current_user"]:
        print("エラー: ログインしてください。")
        return
    
    user_records = [r for r in data["records"] if r["user"] == data["current_user"]]
    total_time = sum(r["duration_seconds"] for r in user_records)
    
    print("=== 学習状況レポート ===")
    print(f"総学習回数: {len(user_records)} 回")
    print(f"総学習時間: {format_time(total_time)}")
    
    # 目標は1分(60秒)として計算
    goal = 60
    progress = min(int((total_time / goal) * 10), 10)
    bar = "■" * progress + "□" * (10 - progress)
    percent = min(int((total_time / goal) * 100), 100)
    print(f"目標達成率: [{bar}] {percent}% (目標: 1分0秒)")


# --- 3. コマンドライン引数の設定 ---
def main():
    parser = argparse.ArgumentParser(description="自作CLI学習管理ソフト")
    subparsers = parser.add_subparsers(dest="command")

    # 認証
    subparsers.add_parser("register", help="新規アカウント作成")
    subparsers.add_parser("login", help="ログイン")

    # タスク
    p_add = subparsers.add_parser("add", help="新しいタスクを登録")
    p_add.add_argument("title", type=str, help="タスクのタイトル")
    p_add.add_argument("--priority", type=str, choices=["高", "中", "低"], default="中", help="優先度")

    subparsers.add_parser("list", aliases=["ls"], help="未完了タスクを一覧表示")
    
    p_done = subparsers.add_parser("done", help="タスクを完了状態にする")
    p_done.add_argument("id", type=int, help="完了にするタスクのID")

    p_delete = subparsers.add_parser("delete", help="タスクを削除する")
    p_delete.add_argument("id", type=int, help="削除するタスクのID")

    # タイマー (第一引数に時間を指定できるように変更、デフォルトはテスト用の15s)
    p_start = subparsers.add_parser("start", help="ポモドーロタイマーの開始")
    p_start.add_argument("time", type=str, nargs="?", default="15s", help="タイマーの時間 (例: 25m, 45s)")
    p_start.add_argument("-t", "--task_id", type=int, default=1, help="対応するタスクのID")

    # レポート
    subparsers.add_parser("summary", aliases=["stats"], help="学習時間の統計を表示")

    args = parser.parse_args()

    if args.command == "register":
        cmd_register(args)
    elif args.command == "login":
        cmd_login(args)
    elif args.command in ["list", "ls"]:
        cmd_list(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "done":
        cmd_done(args)
    elif args.command == "delete":
        cmd_delete(args)
    elif args.command == "start":
        cmd_start(args)
    elif args.command in ["summary", "stats"]:
        cmd_summary(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
