import sys
import csv
import os

DATA_FILE = "movie.csv"

def load_movies():
    movies = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                movies.append(row)
    return movies

def save_movies(movies):
    with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "genre", "rate"])
        writer.writeheader()
        writer.writerows(movies)

def add_movie(title, genre, rate):
    movies = load_movies()
    movies.append({"title": title, "genre": genre, "rate": rate})
    save_movies(movies)
    print("映画を追加しました")

def list_movies():
    movies = load_movies()
    for movie in movies:
        print(f'{movie["title"]} / {movie["genre"]} / 評価:{movie["rate"]}')

def search_movie(keyword):
    movies = load_movies()
    for movie in movies:
        if keyword in movie["title"]:
            print(f'{movie["title"]} / {movie["genre"]} / 評価:{movie["rate"]}')

def delete_movie(title):
    movies = load_movies()
    movies = [movie for movie in movies if movie["title"] != title]
    save_movies(movies)
    print("映画を削除しました")

def edit_movie(title, new_rate):
    movies = load_movies()
    for movie in movies:
        if movie["title"] == title:
            movie["rate"] = new_rate
    save_movies(movies)
    print("映画を編集しました")

def sort_movies():
    movies = load_movies()
    movies.sort(key=lambda x: int(x["rate"]), reverse=True)
    for movie in movies:
        print(f'{movie["title"]} / {movie["genre"]} / 評価:{movie["rate"]}')

args = sys.argv

if len(args) < 2:
    print("コマンドを入力してください")
elif args[1] == "add":
    add_movie(args[2], args[3], args[4])
elif args[1] == "list":
    list_movies()
elif args[1] == "search":
    search_movie(args[2])
elif args[1] == "delete":
    delete_movie(args[2])
elif args[1] == "edit":
    edit_movie(args[2], args[3])
elif args[1] == "sort":
    sort_movies()
else:
    print("不明なコマンドです")
