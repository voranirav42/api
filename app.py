import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_terabox_link(terabox_url):
    # આ Direct API છે, જેમાં Chromium ની જરૂર પડતી નથી
    api_url = "https://terabox-dl.qtcloud.workers.dev/api/get-info"
    params = {"url": terabox_url}
    try:
        response = requests.get(api_url, params=params, timeout=20)
        data = response.json()
        if "download_link" in data:
            return data["download_link"]
        elif "list" in data and len(data["list"]) > 0:
            return data["list"][0].get("download_link")
        return None
    except:
        return None

@app.route('/')
def home():
    return "API is Running Smoothly!"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"success": False, "error": "URL provide kar bhai"}), 400
    
    final_link = get_terabox_link(url)
    if final_link:
        return jsonify({"success": True, "download_link": final_link})
    else:
        return jsonify({"success": False, "error": "Link extraction failed."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
