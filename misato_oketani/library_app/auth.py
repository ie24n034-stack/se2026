import json

USER_FILE = "users.json"


def load_users():
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def register():
    users = load_users()

    user_id = input("ユーザーID: ")
    name = input("名前: ")
    password = input("パスワード: ")

    for u in users:
        if u["user_id"] == user_id:
            print("すでに存在するユーザーです")
            return

    users.append({
        "user_id": user_id,
        "name": name,
        "password": password
    })

    save_users(users)
    print("登録完了")


def login():
    users = load_users()

    user_id = input("ユーザーID: ")
    password = input("パスワード: ")

    for u in users:
        if u["user_id"] == user_id and u["password"] == password:
            print("ログイン成功")
            return u

    print("ログイン失敗")
    return None