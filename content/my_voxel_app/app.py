import json
import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='.')

# ブロック定義 (共通のテクスチャパスを参照)
BLOCK_TYPES = {
    "grass": {"texture": "/common/textures/grass.png"},
    "dirt": {"texture": "/common/textures/dirt.png"},
    "stone": {"texture": "/common/textures/stone.png"},
    "wood": {"texture": "/common/textures/wood.png"}
}

# /common/ へのアクセスでcommonディレクトリからファイルを返す
@app.route('/common/<path:filename>')
def common_files(filename):
    return send_from_directory('common', filename)

# メインページを表示
@app.route('/')
def index():
    return render_template('index.html')

# ブロックの種類をJSONで返すAPI
@app.route('/api/block_types')
def get_block_types():
    return jsonify(BLOCK_TYPES)

# シーンデータをサーバーに保存するAPI
@app.route('/api/save_scene', methods=['POST'])
def save_scene():
    scene_data = request.get_json()
    if not scene_data or 'blocks' not in scene_data:
        return jsonify({"status": "error", "message": "Invalid data"}), 400

    try:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scene_{now}.json"

        with open(filename, "w") as f:
            json.dump(scene_data, f, indent=2)

        print(f"シーンが {filename} として保存されました。")
        return jsonify({"status": "success", "filename": filename})
    except Exception as e:
        print(f"保存エラー: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)