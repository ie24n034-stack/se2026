from auth import login, register
from book import search_book, show_books, get_book_detail


def main():
    user = None

    while True:
        print("\n==== 図書管理アプリ ====")

        if user is None:
            print("1. ログイン")
            print("2. 新規登録")
            print("3. 終了")

            choice = input("選択: ")

            if choice == "1":
                user = login()

            elif choice == "2":
                register()

            elif choice == "3":
                break

            else:
                print("無効な選択")

        else:
            print("1. 本検索")
            print("2. 本一覧")
            print("3. 本詳細")
            print("4. ログアウト")

            choice = input("選択: ")

            if choice == "1":
                search_book()

            elif choice == "2":
                show_books()

            elif choice == "3":
                get_book_detail()

            elif choice == "4":
                user = None
                print("ログアウトしました")

            else:
                print("無効な選択")


if __name__ == "__main__":
    main()