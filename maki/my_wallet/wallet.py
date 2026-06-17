import sys
import csv
import os
from datetime import datetime

CONFIG_FILE = "config.csv"
WALLET_FILE = "wallet.csv"
ENCODING = "utf-8"

def init_files():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w', encoding=ENCODING, newline='') as f:
            csv.writer(f).writerow(['key', 'value'])
    if not os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, 'w', encoding=ENCODING, newline='') as f:
            csv.writer(f).writerow(['id', 'date', 'amount', 'description', 'category'])

def load_budget():
    if not os.path.exists(CONFIG_FILE):
        return 0
    with open(CONFIG_FILE, 'r', encoding=ENCODING) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and row[0] == 'budget':
                return int(row[1])
    return 0

def load_all_expenses():
    expenses = []
    if not os.path.exists(WALLET_FILE):
        return expenses
    with open(WALLET_FILE, 'r', encoding=ENCODING) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row:
                expenses.append({
                    'id': int(row[0]),
                    'date': row[1],
                    'amount': int(row[2]),
                    'description': row[3],
                    'category': row[4]
                })
    return expenses

def save_all_expenses(expenses):
    with open(WALLET_FILE, 'w', encoding=ENCODING, newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'date', 'amount', 'description', 'category'])
        for exp in expenses:
            writer.writerow([exp['id'], exp['date'], exp['amount'], exp['description'], exp['category']])

def cmd_budget(args):
    if len(args) < 1:
        print("エラー: 金額を指定してください。 (例: wallet.py budget 50000)")
        sys.exit(1)
    amount_str = args[0]
    if not amount_str.isdigit():
        print(f"エラー: 金額には正の整数を指定してください: {amount_str}")
        sys.exit(1)
    with open(CONFIG_FILE, 'w', encoding=ENCODING, newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['key', 'value'])
        writer.writerow(['budget', amount_str])
    print(f"今月の予算を {int(amount_str):,} 円に設定しました。")

def cmd_buy(args):
    if len(args) < 2:
        print("エラー: 金額と内容を指定してください。 (例: wallet.py buy 1200 ランチ)")
        sys.exit(1)
    amount_str = args[0]
    description = args[1]
    if not amount_str.isdigit():
        print(f"エラー: 金額には正の整数を指定してください: {amount_str}")
        sys.exit(1)
    if len(args) >= 3:
        category = args[2]
    else:
        print("カテゴリが指定されていません。")
        category = input("カテゴリを入力してください (例: 食費, 交際費) [未分類]: ").strip()
        if not category:
            category = "未分類"
    expenses = load_all_expenses()
    next_id = max([exp['id'] for exp in expenses]) + 1 if expenses else 1
    today_str = datetime.now().strftime("%Y-%m-%d")
    new_expense = {
        'id': next_id,
        'date': today_str,
        'amount': int(amount_str),
        'description': description,
        'category': category
    }
    expenses.append(new_expense)
    save_all_expenses(expenses)
    today_total = sum(exp['amount'] for exp in expenses if exp['date'] == today_str)
    print(f"追加しました（本日合計: {today_total:,}円）")

def cmd_rm(args):
    if len(args) < 1:
        print("エラー: 削除するIDを指定してください。 (例: wallet.py rm 3)")
        sys.exit(1)
    id_str = args[0]
    if not id_str.isdigit():
        print(f"エラー: IDには数値を指定してください: {id_str}")
        sys.exit(1)
    target_id = int(id_str)
    expenses = load_all_expenses()
    exists = any(exp['id'] == target_id for exp in expenses)
    if not exists:
        print(f"エラー: ID {target_id} のデータが見つかりません。")
        sys.exit(1)
    filtered_expenses = [exp for exp in expenses if exp['id'] != target_id]
    save_all_expenses(filtered_expenses)
    print(f"ID {target_id} のデータを削除しました。（他のIDは維持されます）")

def cmd_list():
    current_month = datetime.now().strftime("%Y-%m")
    expenses = load_all_expenses()
    current_expenses = [exp for exp in expenses if exp['date'].startswith(current_month)]
    print(f"=== 【{current_month}】 今月の支出一覧 ===")
    if not current_expenses:
        print("今月の支出データはありません。")
        return
    print(f"{'ID':<4} {'日付':<10} {'金額':<8} {'内容':<16} {'カテゴリ'}")
    print("-" * 60)
    for exp in current_expenses:
        print(f"{exp['id']:<4} {exp['date']:<10} {exp['amount']:<8,} {exp['description']:<16} {exp['category']}")

def cmd_summary():
    current_month = datetime.now().strftime("%Y-%m")
    budget = load_budget()
    expenses = load_all_expenses()
    current_expenses = [exp for exp in expenses if exp['date'].startswith(current_month)]
    total_expense = sum(exp['amount'] for exp in current_expenses)
    balance = budget - total_expense
    status_emoji = "🟢" if balance >= 0 else "🔴"
    print(f"=== 【{current_month}】 今月の収支サマリー ===")
    print(f"  設定予算 : {budget:,} 円")
    print(f"  支出合計 : {total_expense:,} 円")
    print(f"  予算残り : {balance:,} 円 {status_emoji}")
    print()
    print("--- カテゴリ内訳 (高額順) ---")
    category_totals = {}
    for exp in current_expenses:
        cat = exp['category']
        category_totals[cat] = category_totals.get(cat, 0) + exp['amount']
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    if not sorted_categories:
        print("データがありません。")
    for cat, amt in sorted_categories:
        print(f"  {cat:<12} : {amt:,} 円")

def cmd_history():
    expenses = load_all_expenses()
    print("=== 過去すべての履歴 ===")
    if not expenses:
        print("履歴はありません。")
        return
    print(f"{'ID':<4} {'日付':<10} {'金額':<8} {'内容':<16} {'カテゴリ'}")
    print("-" * 60)
    for exp in expenses:
        print(f"{exp['id']:<4} {exp['date']:<10} {exp['amount']:<8,} {exp['description']:<16} {exp['category']}")

def print_usage():
    print("Usage: python wallet.py <サブコマンド> [引数]")
    print("\nサブコマンド:")
    print("  budget <金額>               今月の予算を設定・更新")
    print("  buy <金額> <内容> [カテゴリ] 支出を追加")
    print("  rm <ID>                     指定したIDの支出を削除")
    print("  list                        今月の支出一覧を表示")
    print("  summary                     今月の統計と予算残高を表示")
    print("  history                     過去すべての履歴を表示")

def main():
    init_files()
    args = sys.argv[1:]
    if not args:
        print_usage()
        sys.exit(0)
    subcommand = args[0]
    sub_args = args[1:]
    if subcommand == "budget":
        cmd_budget(sub_args)
    elif subcommand == "buy":
        cmd_buy(sub_args)
    elif subcommand == "rm":
        cmd_rm(sub_args)
    elif subcommand == "list":
        cmd_list()
    elif subcommand == "summary":
        cmd_summary()
    elif subcommand == "history":
        cmd_history()
    else:
        print(f"エラー: 未知のサブコマンド '{subcommand}' です。")
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
