class Timetable:
    def __init__(self):
        self.data = {}

    # 登録
    def add(self, name, day, period, room, teacher):
        if not name:
            return "エラー: 科目名が空です"

        self.data[name] = {
            "day": day,
            "period": period,
            "room": room,
            "teacher": teacher
        }
        return "登録完了"

    # 編集
    def edit(self, name, room, teacher):
        if name in self.data:
            self.data[name]["room"] = room
            self.data[name]["teacher"] = teacher
            return "更新完了"
        return "エラー: 見つかりません"

    # 削除
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return "削除完了"
        return "エラー: 見つかりません"

    # 一覧表示
    def show(self):
        if not self.data:
            return "データなし"

        text = "\n--- 時間割 ---\n"
        for name, v in self.data.items():
            text += f"{name} / {v['day']} {v['period']} / {v['room']} / {v['teacher']}\n"
        return text

    # 共有
    def share(self):
        return "https://share.example.com/my-timetable"


def main():
    app = Timetable()

    while True:
        print("\n1:登録 2:編集 3:削除 4:一覧 5:共有 6:終了")
        c = input("選択: ")

        if c == "1":
            print(app.add(
                input("科目名: "),
                input("曜日: "),
                input("時限: "),
                input("教室: "),
                input("担当: ")
            ))

        elif c == "2":
            print(app.edit(
                input("科目名: "),
                input("教室: "),
                input("担当: ")
            ))

        elif c == "3":
            print(app.delete(input("科目名: ")))

        elif c == "4":
            print(app.show())

        elif c == "5":
            print("共有リンク:", app.share())

        elif c == "6":
            break

        else:
            print("無効")

if __name__ == "__main__":
    main()
