data = []

while True:
    print("\n1:追加  2:表示  3:削除  4:終了")
    choice = input("選んでください: ")

    if choice == "1":
        username = input("ユーザー名: ")
        text = input("データ: ")

        data.append({
            "username": username,
            "data": text
        })

        print("保存しました")

    elif choice == "2":
        print("\n--- データ一覧 ---")

        if len(data) == 0:
            print("データなし")

        for i, item in enumerate(data):
            print(f"{i}: {item['username']} - {item['data']}")

    elif choice == "3":
        num = int(input("削除番号: "))

        if 0 <= num < len(data):
            del data[num]
            print("削除しました")
        else:
            print("番号エラー")

    elif choice == "4":
        print("終了します")
        break

    else:
        print("入力エラー")
