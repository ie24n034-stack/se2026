from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hqnechan-game-secret-2026'
DB_PATH = 'hqne_game.db' # Hqnechan専用のデータベースファイル

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 設計書（design.md）のデータを初期化する
def init_game_db():
    conn = get_db()
    # 1. プレイヤーデータ（座標、HP、所持アイテムなど）
    conn.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        hp INTEGER DEFAULT 100,
        pos_x INTEGER DEFAULT 0,
        pos_y INTEGER DEFAULT 0,
        items TEXT DEFAULT '回復薬, 木の棒'
    )''')
    # 2. ログデータ（チャット履歴など）
    conn.execute('''
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

# 画面1: タイトル画面・サーバー選択
@app.route('/')
def title_screen():
    servers = [
        {"id": "HQ-SV1", "name": "Hqnechan 鯖1 (メイン)", "status": "快適"},
        {"id": "HQ-SV2", "name": "Hqnechan 鯖2 (テスト)", "status": "空いています"}
    ]
    return render_template('title.html', servers=servers)

# ログイン・ゲーム参加処理
@app.route('/join_game', methods=['POST'])
def join_game():
    username = request.form.get('username', '').strip()
    server_id = request.form.get('server_id')
    
    if not username:
        return redirect(url_for('title_screen'))
        
    conn = get_db()
    conn.execute('INSERT OR IGNORE INTO players (username) VALUES (?)', (username,))
    conn.commit()
    conn.close()
    
    session['player_name'] = username
    session['server_id'] = server_id
    return redirect(url_for('main_game'))

# 画面2 & 3: メインゲーム画面・インベントリ・チャット
@app.route('/game')
def main_game():
    if 'player_name' not in session:
        return redirect(url_for('title_screen'))
        
    conn = get_db()
    player = conn.execute('SELECT * FROM players WHERE username = ?', (session['player_name'],)).fetchone()
    conn.close()
    
    inventory = player['items'].split(', ') if player['items'] else []
    
    return render_template('game.html', player=player, inventory=inventory, server_id=session['server_id'])

# 処理の流れ：操作入力（APIパケット送受信） ➔ サーバーへ保存・同期
@app.route('/api/move', methods=['POST'])
def move_player():
    if 'player_name' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    direction = data.get('direction')
    
    conn = get_db()
    player = conn.execute('SELECT pos_x, pos_y FROM players WHERE username = ?', (session['player_name'],)).fetchone()
    
    x, y = player['pos_x'], player['pos_y']
    if direction == 'up': y += 1
    elif direction == 'down': y -= 1
    elif direction == 'left': x -= 1
    elif direction == 'right': x += 1
    
    conn.execute('UPDATE players SET pos_x = ?, pos_y = ? WHERE username = ?', (x, y, session['player_name']))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "new_x": x, "new_y": y})

# ログデータ（チャット）の送受信
@app.route('/api/chat', methods=['POST', 'GET'])
def handle_chat():
    conn = get_db()
    if request.method == 'POST':
        if 'player_name' not in session: return jsonify({"error": "Unauthorized"}), 401
        msg = request.json.get('message', '')
        if msg:
            conn.execute('INSERT INTO chat_logs (username, message, created_at) VALUES (?, ?, ?)', 
                         (session['player_name'], msg, datetime.now().strftime('%H:%M:%S')))
            conn.commit()
        return jsonify({"status": "sent"})
    else:
        logs = conn.execute('SELECT * FROM chat_logs ORDER BY id DESC LIMIT 5').fetchall()
        conn.close()
        return jsonify([{"user": l['username'], "msg": l['message'], "time": l['created_at']} for l in logs])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('title_screen'))

if __name__ == '__main__':
    init_game_db()
    app.run(debug=True, port=5002) # 重複を避けるためポート5002で起動します
