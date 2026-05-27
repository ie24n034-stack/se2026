import json
import os

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def list_tasks(tasks):
    if not tasks:
        print("タスクはありません。")
        return
    print("\n--- タスク一覧 ---")
    for t in tasks:
        status = "✔" if t["status"] else " "
        print(f"[{t['id']}] [{status}] {t['title']}")
    print("-------------------\n")

def add_task(tasks):
    title = input("タスク名を入力： ")
    if not title:
        print("タスク名が空です。")
        return
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": new_id, "title": title, "status": False})
    save_tasks(tasks)
    print("追加しました。")

def delete_task(tasks):
    list_tasks(tasks)
    try:
        task_id = int(input("削除するID： "))
    except ValueError:
        print("数字を入力してください。")
        return
    target = next((t for t in tasks if t["id"] == task_id), None)
    if not target:
        print("そのIDのタスクはありません。")
        return
    confirm = input("本当に削除しますか？（y/n）： ")
    if confirm.lower() != "y":
        print("キャンセルしました。")
        return
    tasks.remove(target)
    save_tasks(tasks)
    print("削除しました。")

def edit_task(tasks):
    list_tasks(tasks)
    try:
        task_id = int(input("編集するID： "))
    except ValueError:
        print("数字を入力してください。")
        return
    target = next((t for t in tasks if t["id"] == task_id), None)
    if not target:
        print("そのIDのタスクはありません。")
        return
    new_title = input("新しいタスク名： ")
    if not new_title:
        print("タスク名が空です。")
        return
    target["title"] = new_title
    save_tasks(tasks)
    print("編集しました。")

def toggle_status(tasks):
    list_tasks(tasks)
    try:
        task_id = int(input("完了状態を切り替えるID： "))
    except ValueError:
        print("数字を入力してください。")
        return
    target = next((t for t in tasks if t["id"] == task_id), None)
    if not target:
        print("そのIDのタスクはありません。")
        return
    target["status"] = not target["status"]
    save_tasks(tasks)
    print("状態を変更しました。")

def main():
    tasks = load_tasks()
    while True:
        print("=== タスク管理 CLI ===")
        print("1. タスク一覧")
        print("2. タスク追加")
        print("3. タスク編集")
        print("4. タスク削除")
        print("5. 完了状態の変更")
        print("0. 終了")
        choice = input("番号を選択： ")
        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            edit_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            toggle_status(tasks)
        elif choice == "0":
            print("終了します。")
            break
        else:
            print("正しい番号を入力してください。")

if __name__ == "__main__":
    main()
