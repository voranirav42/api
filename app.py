import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_link_v1(url):
    try:
        r = requests.get(f"https://terabox-dl.qtcloud.workers.dev/api/get-info?url={url}", timeout=10)
        data = r.json()
        return data.get("download_link") or data.get("list", [{}])[0].get("download_link")
    except:
        return None

def get_link_v2(url):
    try:
        # આ બીજો રસ્તો છે જો પહેલો રસ્તો કામ ના કરે તો
        r = requests.get(f"https://terabox-api.visual-club.workers.dev/api/get-info?url={url}", timeout=10)
        data = r.json()
        return data.get("video_link") or data.get("download_link")
    except:
        return None

@app.route('/')
def home():
    return "TeraBox API is Running Smoothly!"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"success": False, "error": "URL provide kar bhai"}), 400
    
    # પહેલો રસ્તો ટ્રાય કરો
    link = get_link_v1(url)
    
    # જો પહેલો ફેઈલ જાય તો બીજો ટ્રાય કરો
    if not link:
        link = get_link_v2(url)
        
    if link:
        return jsonify({"success": True, "download_link": link})
    else:
        return jsonify({"success": False, "error": "Extraction failed. Try another link or wait."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
