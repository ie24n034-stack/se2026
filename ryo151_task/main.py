import argparse
import sys
import os
import json
from datetime import datetime  # 日付や時刻を扱うためのライブラリです

# データを保存するフォルダとファイルの場所を決めています（設計書通り）
CONFIG_DIR = os.path.expanduser("~/.config/sport-track")
CONFIG_FILE = os.path.join(CONFIG_DIR, "data.json")

def main():
    # --- 1. 窓口（インターフェース）の設定 ---
    parser = argparse.ArgumentParser(description="SportTrack CLI - フィットネストラッカー")
    subparsers = parser.add_subparsers(dest="command", help="利用可能なコマンド")

    subparsers.add_parser("config", help="初期設定を行い、保存領域を作ります")
    subparsers.add_parser("status", help="これまでの全トレーニング履歴を表示します")
    
    run_parser = subparsers.add_parser("run", help="トレーニング記録を追加します")
    # runの後に続く筋トレ内容（文字列）を必須引数として受け取ります
    run_parser.add_argument("input", type=str, help="記録したい内容（例: ベンチプレス 60kg 10回）")

    args = parser.parse_args()

    # --- 2. 各コマンドの実際の処理（ロジック） ---

    # 【config コマンド】
    if args.command == "config":
        print("【INFO】初期設定を開始します...")
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        
        # 最初に作る空っぽのデータ構造
        initial_data = {
            "user": "hr200",
            "created_at": str(datetime.now().date()),
            "history": []  # 最初は履歴は空っぽ
        }
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, indent=4, ensure_ascii=False)
            
        print(f"【SUCCESS】保存ファイルを作成しました: {CONFIG_FILE}")

    # 【run コマンド（記録の追加）】
    elif args.command == "run":
        # 1. もし初期設定（config）がまだされていなかったらエラーを出す安全装置
        if not os.path.exists(CONFIG_FILE):
            print("【ERROR】初期設定がされていません。先に 'python main.py config' を実行してください", file=sys.stderr)
            sys.exit(1)

        # 2. 今あるファイル（data.json）をいったん読み込んで、中に何が入っているか確認する
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 3. 現在の「日付と時刻」をきれいに整形して取得する（例: 2026-05-27 10:30:15）
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 4. 新しい筋トレのデータを1件分、辞書（パーツ）として作る
        new_record = {
            "date": now_str,
            "content": args.input  # ユーザーが画面で打ち込んだ「ベンチプレス〜」の文字
        }

        # 5. 元々あった履歴（history）のリストの一番後ろに、新しいデータを合体（追加）する
        data["history"].append(new_record)

        # 6. 合体した最新のデータを、もう一度ファイルに上書き保存する
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"【SUCCESS】記録を追加しました: [{now_str}] {args.input}")

    # 【status コマンド（履歴の一覧表示）】
    elif args.command == "status":
        if not os.path.exists(CONFIG_FILE):
            print("【ERROR】データファイルが見つかりません。先に config を実行してください", file=sys.stderr)
            sys.exit(1)

        # 1. 保存されているデータを読み込む
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"=== {data['user']} のトレーニング履歴一覧 ===")
        
        # 2. 履歴（history）が空っぽだった場合の処理
        if not data["history"]:
            print("まだ記録がありません。'python main.py run \"[内容]\"' で記録を追加しましょう！")
            return

        # 3. 履歴に入っているデータを、for文（ループ）を使って上から順番にすべて画面に表示する
        for item in data["history"]:
            # item['date'] で日付、item['content'] で筋トレ内容を取り出す
            print(f" 📅 {item['date']} ➔ {item['content']}")
        print("=========================================")

    # コマンドが何も入力されなかったり、間違っている場合
    else:
        parser.print_help()

if __name__ == "__main__":
    main()