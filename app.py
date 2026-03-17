from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
# CORS ઉમેરવું જરૂરી છે, નહીંતર Hostinger પરથી રિક્વેસ્ટ બ્લોક થઈ જશે
CORS(app)

def get_mp4_link(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://teradownloader.com/")
        page.fill('input[type="text"]', url)
        page.click('button[type="submit"]')
        
        try:
            with page.expect_response(lambda response: "/api" in response.url, timeout=15000) as response_info:
                response = response_info.value
                json_data = response.json()
                browser.close()
                return json_data.get("download_link")
        except Exception as e:
            browser.close()
            return None

@app.route('/')
def home():
    return "API is running!"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    terabox_url = data.get('url')
    
    if not terabox_url:
        return jsonify({"error": "Please provide a valid link"}), 400
        
    mp4_link = get_mp4_link(terabox_url)
    
    if mp4_link:
        return jsonify({"success": True, "download_link": mp4_link})
    else:
        return jsonify({"error": "Could not extract link. Try again."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
