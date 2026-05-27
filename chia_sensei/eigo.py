import sys
import csv

DATA_FILE = "data.csv"

def init_file():
    """data.csv が存在しない場合は、ヘッダ付きで新規作成する"""
    try:
        with open(DATA_FILE, "a", encoding="utf-8") as f:
            pass
    except IOError:
        print(f"エラー: {DATA_FILE} の初期化に失敗しました。")

def load_data():
    """data.csv から既存データを読み込む"""
    data = {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0].strip().lower() == "english":
                    continue
                if len(row) >= 2:
                    data[row[0].strip()] = row[1].strip()
    except FileNotFoundError:
        pass
    return data

def save_data(data):
    """データを data.csv に保存する"""
    with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["english", "japanese"])
        for eng, jpn in data.items():
            writer.writerow([eng, jpn])

def main():
    init_file()
    
    # 引数のチェック（スクリプト名とサブコマンド 'add' を除いた数）
    args = sys.argv[2:]
    if len(sys.argv) < 2 or sys.argv[1].lower() != "add":
        print("使い方:")
        print("  python egjz.py add <english> [日本語]")
        print("  python egjz.py add [english] <日本語>  (※どちらか片方でも可)")
        return

    # 既存のデータを読み込み
    data = load_data()

    english = ""
    japanese = ""

    # 引数の数に応じて、入力された値を割り振る
    if len(args) >= 2:
        english = args[0].strip()
        japanese = args[1].strip()
    elif len(args) == 1:
        val = args[0].strip()
        # 簡易判定：アルファベットかそれ以外（日本語など）か
        if val.isascii():
            english = val
        else:
            japanese = val

    # 片方しか指定されていない場合、残りを対話で聞く
    try:
        if not english:
            english = input(f"意味「{japanese}」に対する【英語】を入力してください: ").strip()
        elif not japanese:
            japanese = input(f"単語「{english}」に対する【日本語の意味】を入力してください: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\n入力をキャンセルしました。")
        return

    # バリデーション
    if not english or not japanese:
        print("エラー: 英語と日本語の両方を入力する必要があります。")
        return

    # 既存と重複チェック（editと分離するためのガード）
    if english in data:
        print(f"エラー: '{english}' は既に登録されています。")
        return

    # データの追加と保存
    data[english] = japanese
    save_data(data)
    print(f"追加した（合計{len(data)}単語）")

if __name__ == "__main__":
    main()
