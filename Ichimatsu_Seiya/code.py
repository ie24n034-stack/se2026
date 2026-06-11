tasks = []

while True:
    print("\n=== Task Manager ===")
    print("1. タスク追加")
    print("2. タスク一覧表示")
    print("3. タスク削除")
    print("4. タスク完了切り替え")
    print("5. 終了")

    choice = input("番号を入力してください: ")

    # タスク追加
    if choice == "1":
        title = input("タスク名を入力: ")
        task = {
            "title": title,
            "done": False
        }
        tasks.append(task)
        print("タスクを追加しました")

    # タスク一覧表示
    elif choice == "2":
        if len(tasks) == 0:
            print("タスクがありません")
        else:
            print("\n--- タスク一覧 ---")
            for i, task in enumerate(tasks):
                status = "完了" if task["done"] else "未完了"
                print(f"{i}: {task['title']} [{status}]")

    # タスク削除
    elif choice == "3":
        if len(tasks) == 0:
            print("タスクがありません")
            continue

        for i, task in enumerate(tasks):
            print(f"{i}: {task['title']}")

        try:
            index = int(input("削除する番号: "))
        except ValueError:
            print("数字を入力してください")
            continue

        if 0 <= index < len(tasks):
            del tasks[index]
            print("削除しました")
        else:
            print("無効な番号です")

    # 完了切り替え
    elif choice == "4":
        if len(tasks) == 0:
            print("タスクがありません")
            continue

        for i, task in enumerate(tasks):
            status = "完了" if task["done"] else "未完了"
            print(f"{i}: {task['title']} [{status}]")

        try:
            index = int(input("変更する番号: "))
        except ValueError:
            print("数字を入力してください")
            continue

        if 0 <= index < len(tasks):
            tasks[index]["done"] = not tasks[index]["done"]
            print("状態を変更しました")
        else:
            print("無効な番号です")

    # 終了
    elif choice == "5":
        print("終了します")
        break

    else:
        print("正しい番号を入力してください")
