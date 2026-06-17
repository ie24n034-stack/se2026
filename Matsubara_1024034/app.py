cat << 'EOF' > app.py
import argparse, json, os, time, hashlib, re
from datetime import datetime

DATA_FILE = "storage.json"

def format_time(s): return f"{s//60}分{s%60}秒" if s >= 60 else f"{s}秒"

def parse_time(t):
    m = re.match(r'(?:(\d+)m)?(?:(\d+)s)?', t.lower().strip())
    if m and (m.group(1) or m.group(2)):
        return (int(m.group(1)) if m.group(1) else 0) * 60 + (int(m.group(2)) if m.group(2) else 0)
    try: return int(t)
    except: return 15

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {"users": {}, "tasks": [], "records": [], "current_user": None}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def check_login(data):
    if not data["current_user"]: print("エラー: ログインしてください。")
    return data["current_user"] is not None

def cmd_register(args):
    data = load_data(); name = input("ユーザー名: ")
    if name in data["users"]: return print("エラー: 既に存在します。")
    data["users"][name] = {"password": hash_pw(input("パスワード: ")), "token": None}
    save_data(data); print(f"ユーザー '{name}' の登録が完了しました。")

def cmd_login(args):
    data = load_data(); name, pw = input("ユーザー名: "), input("パスワード: ")
    if name in data["users"] and data["users"][name]["password"] == hash_pw(pw):
        data["users"][name]["token"] = hashlib.md5(str(time.time()).encode()).hexdigest()
        data["current_user"] = name; save_data(data); print(f"ログイン成功！ こんにちは、{name}さん。")
    else: print("エラー: ユーザー名またはパスワードが正しくありません。")

def cmd_add(args):
    data = load_data()
    if not check_login(data): return
    t_id = len(data["tasks"]) + 1
    data["tasks"].append({"task_id": t_id, "title": args.title, "deadline": "2026-06-30", "priority": args.priority, "completed": False, "user": data["current_user"]})
    save_data(data); print(f"タスクを追加しました: [ID: {t_id}] {args.title}")

def cmd_list(args):
    data = load_data()
    if not check_login(data): return
    tasks = [t for t in data["tasks"] if t["user"] == data["current_user"] and not t["completed"]]
    if not tasks: return print("未完了のタスクはありません。")
    print(f"{'ID':<4} | {'タスクタイトル':<25} | {'優先度'}\n" + "-"*45)
    for t in tasks: print(f"{t['task_id']:<4} | {t['title']:<25} | {t['priority']}")

def cmd_done(args):
    data = load_data()
    for t in data["tasks"]:
        if t["task_id"] == args.id and t["user"] == data["current_user"]:
            t["completed"] = True; save_data(data); return print(f"タスク ID {args.id} を完了にしました！")
    print("エラー: 指定されたタスクが見つかりません。")

def cmd_delete(args):
    data = load_data()
    if not check_login(data): return
    orig = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if not (t["task_id"] == args.id and t["user"] == data["current_user"])]
    if len(data["tasks"]) < orig: save_data(data); print(f"タスク ID {args.id} を削除しました。")
    else: print("エラー: 指定されたタスクが見つかりません。")

def cmd_start(args):
    data = load_data()
    if not check_login(data): return
    rem = parse_time(args.time); dur, start_t = rem, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"タイマーを開始します ({format_time(rem)})... [Ctrl+C]で一時停止")
    try:
        while rem > 0: print(f"\r残り時間: {format_time(rem)}    ", end="", flush=True); time.sleep(1); rem -= 1
    except KeyboardInterrupt:
        print("\n\n--- タイマー一時停止 ---")
        if input("再開しますか？ (y/n): ").strip().lower() == 'y':
            try:
                while rem > 0: print(f"\r残り時間: {format_time(rem)}    ", end="", flush=True); time.sleep(1); rem -= 1
            except KeyboardInterrupt: return print("\nタイマーが中断されました。")
        else: return print("タイマーを終了しました。")
    print("\n時間です！休憩に入りましょう。")
    data["records"].append({"record_id": len(data["records"])+1, "start_time": start_t, "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "duration_seconds": dur, "task_id": args.task_id, "user": data["current_user"]})
    save_data(data)

def cmd_summary(args):
    data = load_data()
    if not check_login(data): return
    recs = [r for r in data["records"] if r["user"] == data["current_user"]]
    tot = sum(r["duration_seconds"] for r in recs)
    print(f"=== 学習状況レポート ===\n総学習回数: {len(recs)} 回\n総学習時間: {format_time(tot)}")
    bar = "■" * min(tot//6, 10) + "□" * (10 - min(tot//6, 10))
    print(f"目標達成率: [{bar}] {min(tot*100//60, 100)}% (目標: 1分0秒)")

def main():
    parser = argparse.ArgumentParser(description="自作CLI学習管理ソフト")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("register"); sub.add_parser("login")
    p_add = sub.add_parser("add"); p_add.add_argument("title"); p_add.add_argument("--priority", choices=["高", "中", "低"], default="中")
    sub.add_parser("list", aliases=["ls"])
    for cmd in ["done", "delete"]: p = sub.add_parser(cmd); p.add_argument("id", type=int)
    p_st = sub.add_parser("start"); p_st.add_argument("time", nargs="?", default="15s"); p_st.add_argument("-t", "--task_id", type=int, default=1)
    sub.add_parser("summary", aliases=["stats"])
    
    args = parser.parse_args()
    cmds = {"register": cmd_register, "login": cmd_login, "add": cmd_add, "list": cmd_list, "ls": cmd_list, "done": cmd_done, "delete": cmd_delete, "start": cmd_start, "summary": cmd_summary, "stats": cmd_summary}
    if args.command in cmds: cmds[args.command](args)
    else: parser.print_help()

if __name__ == "__main__": main()
EOF
