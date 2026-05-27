import argparse
import json
import os
import time
import hashlib
from datetime import datetime

# データ設計に基づき、ローカルのJSONファイルにデータを保存します
DATA_FILE = "storage.json"

# --- 1. データ管理用の関数（データストレージ設計） ---
def load_data():
    """JSONファイルからデータを読み込む（ファイルがない場合は初期構造を返す）"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    # 初期データ構造（design.mdのデータ設計に準拠）
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
    
    # パスワードは必ずハッシュ化して保存
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
        # 認証トークン（簡易的にタイムスタンプをハッシュ化したもの）を発行
        token = hashlib.md5(str(time.time()).encode()).hexdigest()
        data["users"][username]["token"] = token
        data["current_user"] = username
        save_data(data)
        print(f"ログイン成功！ こんにちは、{username}さん。 (Token: {token})")
    else:
        print("エラー: ユーザー名またはパスワードが正しくありません。")

def cmd_add(args):
    """学習タスク追加 (add)"""
    data = load_data()
    if not data["current_user"]:
        print("エラー: タスクを追加するには先にログインしてください。")
        return
    
    # タスクIDの自動採番
    task_id = len(data["tasks"]) + 1
    new_task = {
        "task_id": task_id,
        "title": args.title,
        "deadline": "2026-06-30", # 簡易的な締切日
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
    
    # 操作性要件：綺麗なテーブル形式で表示
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

def cmd_start(args):
    """学習タイマー機能 (start)"""
    data = load_data()
    if not data["current_user"]:
        print("エラー: ログインしてください。")
        return
    
    # 授業のテスト用に、デフォルトを25分ではなく「10秒」にしています（引数 -s で変更可能）
    duration = args.seconds
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"ポモドーロタイマーを開始します ({duration}秒)...")
    try:
        for i in range(duration, 0, -1):
            # \r を使うことで同じ行でカウントダウンを表示します
            print(f"\r残り時間: {i}秒 ", end="", flush=True)
            time.sleep(1)
        
        # タイマー終了処理
        print("\n\a時間です！休憩に入りましょう。") # \a はターミナルベル音(環境による)
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 学習記録情報の保存
        record_id = len(data["records"]) + 1
        new_record = {
            "record_id": record_id,
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": duration,
            "user": data["current_user"]
        }
        data["records"].append(new_record)
        save_data(data)
        print("学習記録を保存しました。")
        
    except KeyboardInterrupt:
        print("\nタイマーが中断されました。")

def cmd_summary(args):
    """学習履歴・進捗確認機能 (summary / stats)"""
    data = load_data()
    if not data["current_user"]:
        print("エラー: ログインしてください。")
        return
    
    user_records = [r for r in data["records"] if r["user"] == data["current_user"]]
    total_time = sum(r["duration_seconds"] for r in user_records)
    
    print("=== 学習状況レポート ===")
    print(f"総学習回数: {len(user_records)} 回")
    print(f"総学習時間: {total_time} 秒")
    
    # 操作性要件：達成率をアスキーアートの進捗バーで表示
    # 例として目標を60秒（1分）とした場合の進捗バー
    goal = 60
    progress = min(int((total_time / goal) * 10), 10)
    bar = "■" * progress + "□" * (10 - progress)
    percent = min(int((total_time / goal) * 100), 100)
    print(f"目標達成率: [{bar}] {percent}% (目標: 60秒)")


# --- 3. コマンドライン引数の設定（インターフェース設計） ---
def main():
    # argparseを使うことで、自動的に高機能な --help オプションが生成されます
    parser = argparse.ArgumentParser(description="自作CLI学習管理ソフト")
    subparsers = parser.add_subparsers(dest="command")

    # auth関連
    subparsers.add_parser("register", help="新規アカウント作成")
    subparsers.add_parser("login", help="ログイン")

    # タスク関連
    p_add = subparsers.add_parser("add", help="新しいタスクを登録")
    p_add.add_argument("title", type=str, help="タスクのタイトル")
    p_add.add_argument("--priority", type=str, choices=["高", "中", "低"], default="中", help="優先度")

    # 操作性要件：「list」の代わりに短い「ls」でも動くようにaliasesを設定
    subparsers.add_parser("list", aliases=["ls"], help="未完了タスクを一覧表示")
    
    p_done = subparsers.add_parser("done", help="タスクを完了状態にする")
    p_done.add_argument("id", type=int, help="完了にするタスクのID")

    # タイマー関連
    p_start = subparsers.add_parser("start", help="ポモドーロタイマーの開始")
    p_start.add_argument("-s", "--seconds", type=int, default=10, help="タイマーの時間(秒)")

    # レポート関連
    subparsers.add_parser("summary", aliases=["stats"], help="学習時間の統計をグラフ表示")

    args = parser.parse_args()

    # コマンドの振り分け実行
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
    elif args.command == "start":
        cmd_start(args)
    elif args.command in ["summary", "stats"]:
        cmd_summary(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
