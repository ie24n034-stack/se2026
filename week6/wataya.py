# 検索機能を追加する (#1)
data = ["apple", "banana", "orange"]

word = input("検索したい文字を入力: ")

if word in data:
    print("検索結果: 見つかりました")
else:
    print("検索結果: 見つかりません")


# データをファイル保存できるようにする (#2)
with open("data.txt", "w") as f:
    f.write(word)

print("データを data.txt に保存しました")


# エラーメッセージを分かりやすくする (#3)
num = input("数字を入力してください: ")

try:
    num = int(num)
    print("2倍すると:", num * 2)
except:
    print("エラー: 数字を入力してください")
