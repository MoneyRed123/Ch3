from flask import Flask, request, redirect
import os
from datetime import datetime

app = Flask(__name__)

# データを保存するファイル --- (*1)
データファイル = './board-data.txt'

# ルートページ（メッセージ一覧） --- (*2)
@app.route('/')
def インデックス():
    メッセージリスト = []  # 複数のメッセージを格納
    if os.path.exists(データファイル):
        with open(データファイル, 'rt', encoding='utf-8') as f:
            メッセージリスト = f.readlines()

    # メッセージボードの表示 --- (*3)
    return f"""
    <html><body>
    <h1>メッセージボード</h1>
    <div style="background-color:yellow;padding:1em;">
    {"<br>".join(メッセージリスト) if メッセージリスト else "まだ書き込みはありません。"}
    </div>
    <h3>メッセージを投稿:</h3>
    <form action="/書き込み" method="POST">
        名前: <input type="text" name="名前" required><br/>
        <textarea name="メッセージ" rows="4" cols="50" required></textarea><br/>
        <input type="submit" value="投稿">
    </form>
    </body></html>
    """

# メッセージを書き込む処理 --- (*4)
@app.route('/書き込み', methods=['POST'])
def 書き込み():
    名前 = request.form.get('名前', '匿名').strip()  # ユーザーの名前（未入力なら匿名）
    メッセージ = request.form.get('メッセージ', '').strip()  # メッセージ内容

    if メッセージ:
        タイムスタンプ = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        新しいメッセージ = f"{タイムスタンプ} - {名前}: {メッセージ}\n"

        # メッセージをファイルに追加保存 --- (*5)
        with open(データファイル, 'a', encoding='utf-8') as f:
            f.write(新しいメッセージ)

    return redirect('/')

# アプリを起動 --- (*6)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
