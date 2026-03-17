import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_terabox_link(url):
    # Direct API logic - No browser needed
    api_url = f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={url}"
    try:
        r = requests.get(api_url, timeout=15)
        data = r.json()
        return data.get("download_link") or data.get("list", [{}])[0].get("download_link")
    except:
        return None

@app.route('/')
def home():
    return "API is Running Without Chromium!"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"success": False, "error": "URL provide kar bhai"}), 400

    link = get_terabox_link(url)
    if link:
        return jsonify({"success": True, "download_link": link})
    return jsonify({"success": False, "error": "Extraction failed. Try again."})
