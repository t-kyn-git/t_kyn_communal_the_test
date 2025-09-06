import base64
import datetime
import re
from flask import Flask, render_template, request, jsonify

# Flaskアプリケーションを作成
app = Flask(__name__, template_folder='.')

# ルートURL ('/') にアクセスがあった場合の処理
@app.route('/')
def index():
    # 'index.html' というファイルをブラウザに返す
    return render_template('index.html')

# '/save' というURLにPOSTメソッドでデータが送られてきた場合の処理
@app.route('/save', methods=['POST'])
def save():
    try:
        # ブラウザから送られてきたJSONデータを取得
        data = request.get_json()
        # JSONデータの中から'image_data'キーの値（Base64文字列）を取得
        image_data = data['image_data']

        # Base64文字列のヘッダー部分 'data:image/png;base64,' を取り除く
        header, encoded = image_data.split(",", 1)
        # Base64データをデコードしてバイナリデータに戻す
        image_binary = base64.b64decode(encoded)

        # 現在の日時を使ってファイル名を生成 (例: 20250907_153000.png)
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{now}.png"

        # バイナリ書き込みモード('wb')でファイルを開き、データを書き込む
        with open(filename, "wb") as f:
            f.write(image_binary)

        # 成功したことをブラウザに伝える
        print(f"画像が {filename} として保存されました。") # サーバーのコンソールに表示
        return jsonify({'status': 'success', 'filename': filename})

    except Exception as e:
        # エラーが発生した場合
        print(f"エラーが発生しました: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


# サーバーを起動
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)