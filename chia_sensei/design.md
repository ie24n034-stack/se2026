# 設計

## 画面(入出力の例)
python egjz.py <サブコマンド> [引数]

### サブコマンド：
- add <english> [日本語]    単語を追加
- import <ファイル>         .txt / .csv から一括取り込み
- edit <english>           単語を編集
- rm <english>             単語を削除
- list                     単語一覧
- quiz                     クイズ開始
- stats                    統計を表示

### 実行サンプル：
```
$python egjz.py add dog 犬/いぬ
追加した（合計1単語）
$python egjz.py quiz
Q1: appleは？
$りんご
正解（登録：りんご/リンゴ/林檎）
```

## データ
### data.csv
1つの英単語に対して、日本語の意味を / 区切りで複数保存できる。
```
english, japanese
apple,リンゴ/りんご/林檎
bear,熊/くま
cat,猫/ネコ
```
### history.csv
クイズの結果を残す。
```
date, score, total
2025-05-13,4,10
```
### 取り込み用ファイル
.csvも.txt も同じ扱い。カンマ区切り。

データ例：
```
apple,りんご
bear,熊
```
ヘッダ行（"english,japanese"）があれば自動でスキップする。

## 処理の流れ
### add
1. 引数からenglish（japanese があれば）を取る
2. japaneseが無ければ対話で聞く
3. data.csvを読む
4. 同じenglishが既にあれば、エラーで止める（変更したい場合はeditを使う）
5. 追加して書き戻す
   
### import
1. ファイルを読む（.csv/.txtどちらも可）
2. 1行目がヘッダなら（"english"を含む）スキップ
3. 各行をenglishとjapaneseに分解
4. 既存と重複しないものだけ追加
5. 追加件数を表示
   
### edit
### rm
### list
### quiz
### stats

## 構成
- egjz.py      実装本体
- data.csv     単語データ
- history.csv  クイズ履歴

文字コード：UTF-8固定
ライブラリ：Python標準ライブラリのみ
