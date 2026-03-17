import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_terabox_link(terabox_url):
    # આ એક થર્ડ પાર્ટી API નો ઉપયોગ કરે છે જે બ્રાઉઝર વગર લિંક આપે છે
    api_url = "https://terabox-dl.qtcloud.workers.dev/api/get-info"
    
    params = {
        "url": terabox_url
    }
    
    try:
        response = requests.get(api_url, params=params, timeout=20)
        data = response.json()
        
        # લિંક ચેક કરો
        if "download_link" in data:
            return data["download_link"]
        elif "list" in data and len(data["list"]) > 0:
            return data["list"][0].get("download_link")
        
        return None
    except Exception as e:
        print(f"Request Error: {e}")
        return None

@app.route('/')
def home():
    return "Terabox API is Live (No Browser Mode)!"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"success": False, "error": "No URL provided"}), 400
        
    final_link = get_terabox_link(url)
    
    if final_link:
        return jsonify({"success": True, "download_link": final_link})
    else:
        return jsonify({"success": False, "error": "Could not extract link. The service might be down."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
