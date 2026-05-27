# --- 仮のデータ ---
books = [
    {"title": "Python入門", "author": "山田", "available": True},
    {"title": "AI基礎", "author": "佐藤", "available": False},
    {"title": "データ構造", "author": "田中", "available": True}
]

users = {
    "user1": "pass1",
    "user2": "pass2"
}

# --- ログイン機能 ---
def login():
    user_id = input("ユーザーID: ")
    password = input("パスワード: ")

    if user_id in users and users[user_id] == password:
        print("ログイン成功")
        return True
    else:
        print("ログイン失敗")
        return False


# --- 本検索機能 ---
def search_book(keyword):
    print("検索結果:")
    for book in books:
        if keyword in book["title"] or keyword in book["author"]:
            print(book["title"], "-", book["author"])


# --- 予約機能 ---
def reserve_book(title):
    for book in books:
        if book["title"] == title:
            if not book["available"]:
                print("予約しました:", title)
                return
            else:
                print("この本は貸出可能です（予約不要）")
                return
    print("本が見つかりません")


# --- メイン処理 ---
if login():
    keyword = input("検索キーワード: ")
    search_book(keyword)

    book_name = input("予約したい本のタイトル: ")
    reserve_book(book_name)