import json

BOOK_FILE = "books.json"


def load_books():
    with open(BOOK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_books(books):
    with open(BOOK_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def show_books():
    books = load_books()

    for b in books:
        print(f"{b['id']} | {b['title']} | {b['author']} | {b['status']}")


def search_book():
    keyword = input("検索ワード: ")
    
    if keyword.strip() == "":
        print("検索ワードを入力してください")
        return

    books = load_books()

    found = False

    for b in books:
        if keyword in b["title"] or keyword in b["author"]:
            print("ID:", b["id"])
            print("タイトル:", b["title"])
            print("著者:", b["author"])
            print("状態:", b["status"])
            print("--------")
            found = True

    if not found:
        print("該当する本が見つかりませんでした")


def get_book_detail():
    book_id = input("本ID: ")

    if not book_id.isdigit():
        print("数字を入力してください")
        return

    book_id = int(book_id)
    books = load_books()

    for b in books:
        if b["id"] == book_id:
            print("タイトル:", b["title"])
            print("著者:", b["author"])
            print("状態:", b["status"])
            print("返却予定日:", b["return_date"])
            return

    print(f"本ID{book_id}は登録されていません")