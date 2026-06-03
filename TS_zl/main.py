import sqlite3
import os
import sys
from datetime import datetime

DB_FILE = "todo_cli.db"

def init_db():
    """データベースの初期化"""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_completed INTEGER DEFAULT 0,
                due_date TEXT,
                is_important INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def get_todos(sort_by="id"):
    """タスク一覧を取得"""
    order_query = "id ASC"
    if sort_by == "due_date":
        # 締め切りが近い順（未設定は後ろに回す）
        order_query = "CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END, due_date ASC"
    elif sort_by == "important":
        order_query = "is_important DESC, id ASC"

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM todos ORDER BY {order_query}")
        return cursor.fetchall()

def add_todo():
    """1. タスクの追加"""
    print("\n--- 📝 新しいタスクの追加 ---")
    title = input("タスク名を入力: ").strip()
    if not title:
        print("❌ タスク名が空です。")
        return

    due_date = input("締め切り (YYYY-MM-DD) [省略時はEnter]: ").strip()
    if due_date:
        try:
            # 日付フォーマットの簡易チェック
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("❌ 日付の形式が正しくありません (例: 2026-05-27)。登録を中断します。")
            return

    important_input = input("重要マーク（星）をつけますか？ (y/N): ").strip().lower()
    is_important = 1 if important_input == 'y' else 0

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, due_date, is_important) VALUES (?, ?, ?)",
            (title, due_date, is_important)
        )
        conn.commit()
    print(f"✨ 「{title}」を追加しました！")

def show_todo_list(sort_by="id"):
    """タスクの一覧表示"""
    rows = get_todos(sort_by)
    
    sort_labels = {"id": "追加順", "due_date": "⏳ 締め切り順", "important": "⭐ 重要度順"}
    print(f"\n================【 タスク一覧 ({sort_labels[sort_by]}) 】================")
    print(f"{'ID':<4} {'状態':<4} {'重要':<4} {'タスク名':<25} {'締め切り':<10}")
    print("-" * 60)

    if not rows:
        print("タスクは登録されていません。")
        return

    for r in rows:
        # 見た目の装飾
        status = "✅" if r["is_completed"] else "🔲"
        star = "⭐" if r["is_important"] else "  "
        due = r["due_date"] if r["due_date"] else "---"
        
        # 完了済みは少し暗く（ターミナル表示用）
        title = r["title"]
        if r["is_completed"]:
            title = f"\033[90m{title} (完了済)\033[0m"

        print(f"{r['id']:<4} {status:<4} {star:<4} {title:<25} {due:<10}")
    print("================================================================")

def toggle_complete():
    """2. タスクの完了チェック / 外す"""
    show_todo_list()
    try:
        todo_id = int(input("\n完了/未完了を切り替えるタスクのIDを入力してください: "))
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT is_completed FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            if row is None:
                print("❌ 指定されたIDが見つかりません。")
                return
            
            # 状態を反転
            new_status = 0 if row[0] == 1 else 1
            cursor.execute("UPDATE todos SET is_completed = ? WHERE id = ?", (new_status, todo_id))
            conn.commit()
        print(f"🔄 ID {todo_id} の状態を更新しました。")
    except ValueError:
        print("❌ 有効な数字を入力してください。")

def edit_todo():
    """3. 登録したタスクを後から修正"""
    show_todo_list()
    try:
        todo_id = int(input("\n修正したいタスクのIDを入力してください: "))
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            if row is None:
                print("❌ 指定されたIDが見つかりません。")
                return

            print(f"\n--- 現在のデータ ---")
            print(f"タイトル: {row['title']}\n締め切り: {row['due_date']}\n重要(1=はい/0=いいえ): {row['is_important']}")
            print("-" * 20)
            print("※変更しない場合は何も入力せずにEnterを押してください。")

            new_title = input(f"新しいタスク名 [{row['title']}]: ").strip() or row['title']
            new_due = input(f"新しい締め切り (YYYY-MM-DD) [{row['due_date']}]: ").strip() or row['due_date']
            new_imp_input = input(f"重要にしますか？ (y/n) [{'y' if row['is_important'] else 'n'}]: ").strip().lower()
            
            new_imp = row['is_important']
            if new_imp_input == 'y': new_imp = 1
            elif new_imp_input == 'n': new_imp = 0

            cursor.execute(
                "UPDATE todos SET title = ?, due_date = ?, is_important = ? WHERE id = ?",
                (new_title, new_due, new_imp, todo_id)
            )
            conn.commit()
        print(f"💾 ID {todo_id} のタスクを修正しました。")
    except ValueError:
        print("❌ 有効な数字を入力してください。")

def delete_completed():
    """4. 完了したタスクの一括削除"""
    confirm = input("\n⚠️ 完了済みのタスクをすべて削除しますか？ (y/N): ").strip().lower()
    if confirm == 'y':
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM todos WHERE is_completed = 1")
            conn.commit()
            print(f"🗑️ 完了タスクを削除しました（削除件数: {cursor.rowcount}件）")
    else:
        print("キャンセルしました。")

def main():
    init_db()
    current_sort = "id"

    while True:
        show_todo_list(sort_by=current_sort)
        print("\n[操作メニュー]")
        print(" 1: ➕ 新しいタスクを追加する")
        print(" 2:  タスクの状態（完了/未完了）を切り替える")
        print(" 3: ✏️ タスクを後から修正する")
        print(" 4: 🗑️ 完了したタスクを一括削除する")
        print(" s1: 🔁 追加順に並び替え")
        print(" s2: ⏳ 締め切り順に並び替え")
        print(" s3: ⭐ 重要度順に並び替え")
        print(" q:  ❌ アプリを終了する")
        
        choice = input("\nメニューを選択してください: ").strip().lower()

        if choice == "1":
            add_todo()
        elif choice == "2":
            toggle_complete()
        elif choice == "3":
            edit_todo()
        elif choice == "4":
            delete_completed()
        elif choice == "s1":
            current_sort = "id"
        elif choice == "s2":
            current_sort = "due_date"
        elif choice == "s3":
            current_sort = "important"
        elif choice == "q":
            print("\nアプリを終了します。お疲れ様でした！")
            break
        else:
            print("\n❌ 正しいメニューを入力してください。")
            input("\nEnterを押してメニューに戻る...")

if __name__ == "__main__":
    main()
