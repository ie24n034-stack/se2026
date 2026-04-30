# 設計書：図書管理アプリ

## 画面の説明（3つ）
1. **ホーム画面**: ダッシュボード形式。未読本の数や返却期限が近い本の通知を表示。
2. **一覧画面**: スクロール可能なカード型リスト。サムネイル画像とタイトルを並べる。
3. **詳細画面**: 本のあらすじ、登録日、貸出相手の名前を入力するフォーム。

## データの定義（3つ）
1. **Book（書籍データ）**:
   - id (int), title (string), author (string), status (string)
2. **User（ユーザーデータ）**:
   - user_id (int), name (string), email (string)
3. **RentalLog（貸出履歴データ）**:
   - log_id (int), book_id (int), borrower_name (string), rental_date (date)

## 処理の流れ（1つ）
- **書籍登録の流れ**:
  1. ユーザーが「追加ボタン」を押す。
  2. ISBN入力または手動入力フォームが表示される。
  3. 入力後「保存」を押すと、バリデーション（空欄チェック）が走る。
  4. データベースに保存され、一覧画面へ遷移する。

## システム構成
- **フロントエンド**: React (Web) または Flutter (Mobile)
- **バックエンド**: Node.js + Express
- **データベース**: SQLite (軽量な個人利用を想定)
- **インフラ**: Vercel または Firebase