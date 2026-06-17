from flask import Flask, request, render_template_string, redirect
import json, os

app = Flask(__name__)
FILE = "data.json"  # データ保存ファイル

# 画面の見た目
HTML = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<h2>スケジュール帳</h2>

<form action="/add" method="POST">
    予定: <input type="text" name="title" required>
    期限: <input type="date" name="deadline">
    <button>追加</button>
</form>
<hr>

<ul>
    {% for t in tasks %}
        <li>
            {{ t.title }} (期限: {{ t.deadline }}) - 状態: {{ t.status }}
            <a href="/toggle/{{ t.id }}">🔄切替</a> | 
            <a href="/delete/{{ t.id }}">❌削除</a>
        </li>
    {% else %}
        <p>予定はありません。</p>
    {% endfor %}
</ul>
"""

# データ読み込み・保存機能
def load_data():
    return json.load(open(FILE, "r", encoding="utf-8")) if os.path.exists(FILE) else []

def save_data(data):
    json.dump(data, open(FILE, "w", encoding="utf-8"))

# ① トップページの表示
@app.route("/")
def index():
    return render_template_string(HTML, tasks=load_data())

# ② 予定の追加処理
@app.route("/add", methods=["POST"])
def add():
    tasks = load_data()
    tasks.append({
        "id": len(tasks) + 1, 
        "title": request.form.get("title"), 
        "deadline": request.form.get("deadline") or "未設定",
        "status": "未完了"
    })
    save_data(tasks)
    return redirect("/")

# ③ 状態の切り替え処理
@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    tasks = load_data()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "完了" if t["status"] == "未完了" else "未完了"
    save_data(tasks)
    return redirect("/")

# ④ 予定の削除処理
@app.route("/delete/<int:task_id>")
def delete(task_id):
    save_data([t for t in load_data() if t["id"] != task_id])
    return redirect("/")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
