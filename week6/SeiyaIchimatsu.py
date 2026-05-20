import json
import os
from datetime import datetime

# 保存先ファイル名
DATA_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()  # 起動時にタスク保存機能から読み込み

    # --- 機能3: タスク保存機能 (読み込み / 保存) ---
    def load_tasks(self):
        """ファイルを読み込んでタスクリストを復元する"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except json.JSONDecodeError:
                print("データの読み込みに失敗しました。新規作成します。")
                self.tasks = []

    def save_tasks(self):
        """現在のタスクリストをファイルに保存する"""
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        print("データを保存しました。")

    # --- 機能2: 期限付きタスク追加機能 ---
    def add_task(self, title, deadline_str=None):
        """期限付きのタスクを追加する"""
        task = {
            "title": title,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "deadline": deadline_str if deadline_str else "なし"
        }
        self.tasks.append(task)
        print(f"タスク『{title}』を追加しました。(期限: {task['deadline']})")
        self.save_tasks()  # 変更時に自動保存

    # --- 機能1: タスク検索機能 ---
    def search_tasks(self, keyword):
        """キーワードでタスクを検索して表示する"""
        print(f"\n🔍 『{keyword}』の検索結果:")
        results = [t for t in self.tasks if keyword.lower() in t["title"].lower()]
        
        if not results:
            print("一致するタスクが見つかりませんでした。")
            return

        for i, task in enumerate(results, 1):
            print(f"{i}. [{task['deadline']}] {task['title']}")

    def show_all_tasks(self):
        """すべてのタスクを表示する"""
        print("\n📋 タスク一覧:")
        if not self.tasks:
            print("タスクはありません。")
            return
        for i, task in enumerate(self.tasks, 1):
            print(f"{i}. [{task['deadline']}] {task['title']}")


# --- 動作確認用のメイン処理 ---
if __name__ == "__main__":
    manager = TaskManager()

    print("--- 1. 初期状態表示 ---")
    manager.show_all_tasks()

    print("\n--- 2. タスク追加 (期限付きタスク機能の確認) ---")
    # 期限なしと期限ありのタスクを追加
    manager.add_task("Pythonの課題を提出する", "2026-05-25")
    manager.add_task("牛乳を買う")
    manager.add_task("GitのPRを出す", "2026-05-21")

    print("\n--- 3. タスク検索 (タスク検索機能の確認) ---")
    manager.search_tasks("Python")
    manager.search_tasks("買う")

    print("\n--- 4. 最終タスク一覧 ---")
    manager.show_all_tasks()
