import json
import os

def load_data(username):
    """ユーザーごとのタスクデータを読み込む（非機能3）"""
    filename = f"tasks_{username}.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(username, tasks):
    """ユーザーごとのタスクデータを保存する（非機能3）"""
    filename = f"tasks_{username}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def main():
    print("--- タスク管理CLIツール ---")
    
    # 機能1: ユーザー名を入力してログインできる
    username = input("ユーザー名を入力してください: ").strip()
    if not username:
        print("エラー: ユーザー名が空です。プログラムを終了します。") # 非機能4
        return
        
    print(f"\nこんにちは、{username} さん！ログインしました。")
    tasks = load_data(username)

    # design.md: 終了命令が入力されるまで繰り返す
    while True:
        print("\n[コマンド一覧] add / list / detail / search / edit / delete / exit")
        user_input = input("コマンドを入力してください: ").strip()
        
        if not user_input:
            continue
            
        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        # 終了処理
        if command == "exit":
            print("プログラムを終了します。")
            break

        # 機能2: タスクを登録できる
        elif command == "add":
            if not argument:
                print("エラー: タスクのタイトルを入力してください。（例: add 宿題をする）") # 非機能4
                continue
            detail = input("タスクの詳細情報を入力してください: ").strip()
            
            task_item = {
                "title": argument,
                "detail": detail if detail else "（詳細なし）"
            }
            tasks.append(task_item)
            save_data(username, tasks)
            print(f"成功: タスク「{argument}」を登録しました。")

        # 機能3: 登録したタスク一覧を表示できる
        elif command == "list":
            if not tasks:
                print("登録されているタスクはありません。")
                continue
            print(f"\n--- {username} さんのタスク一覧 ---")
            for i, task in enumerate(tasks, 1):
                print(f"[{i}] {task['title']}")

        # 機能5: タスクの詳細情報を表示できる
        elif command == "detail":
            if not argument or not argument.isdigit():
                print("エラー: 詳細を見たいタスクの番号を指定してください。（例: detail 1）")
                continue
            idx = int(argument) - 1
            if 0 <= idx < len(tasks):
                print(f"\n--- タスク詳細 [{argument}] ---")
                print(f"タイトル: {tasks[idx]['title']}")
                print(f"詳細内容: {tasks[idx]['detail']}")
            else:
                print("エラー: 指定された番号のタスクが見つかりません。")

        # 機能4: タスクを検索できる
        elif command == "search":
            if not argument:
                print("エラー: 検索キーワードを入力してください。（例: search 宿題）")
                continue
            print(f"\n--- 「{argument}」の検索結果 ---")

            search_word = argument.lower()
            found = False
            for i, task in enumerate(tasks, 1):
                if argument in task['title'].lower() or search_word in task['detail'].lower():
                    print(f"[{i}] {task['title']}")
                    found = True
            if not found:
                print("一致するタスクはありませんでした。")

        # 機能6: タスクを編集できる
        elif command == "edit":
            if not argument or not argument.isdigit():
                print("エラー: 編集したいタスクの番号を指定してください。（例: edit 1）")
                continue
            idx = int(argument) - 1
            if 0 <= idx < len(tasks):
                new_title = input(f"新しいタイトル（空欄のままで維持: {tasks[idx]['title']}）: ").strip()
                new_detail = input(f"新しい詳細（空欄のままで維持: {tasks[idx]['detail']}）: ").strip()
                
                if new_title:
                    tasks[idx]['title'] = new_title
                if new_detail:
                    tasks[idx]['detail'] = new_detail
                    
                save_data(username, tasks)
                print("成功: タスクを更新しました。")
            else:
                print("エラー: 指定された番号のタスクが見つかりません。")

        # 機能6: タスクを削除できる
        elif command == "delete":
            if not argument or not argument.isdigit():
                print("エラー: 削除したいタスクの番号を指定してください。（例: delete 1）")
                continue
            idx = int(argument) - 1
            if 0 <= idx < len(tasks):
                removed = tasks.pop(idx)
                save_data(username, tasks)
                print(f"成功: タスク「{removed['title']}」を削除しました。")
            else:
                print("エラー: 指定された番号のタスクが見つかりません。")

        # 非機能4: エラー時のメッセージ表示
        else:
            print(f"エラー: 無効なコマンドです「{command}」")

if __name__ == "__main__":
    main()
