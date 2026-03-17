import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from playwright.sync_api import sync_playwright

app = Flask(__name__)
CORS(app)

# Render પર બ્રાઉઝર ક્યાં સેવ થાય છે તેનો પાથ
PLAYWRIGHT_BROWSERS_PATH = "/opt/render/.cache/ms-playwright"
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = PLAYWRIGHT_BROWSERS_PATH

def get_mp4_link(url):
    with sync_playwright() as p:
        try:
            # બ્રાઉઝર લોન્ચ કરતી વખતે પાથ ચેક કરશે
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://teradownloader.com/", timeout=60000)
            page.fill('input[type="text"]', url)
            page.click('button[type="submit"]')
            
            with page.expect_response(lambda response: "/api" in response.url, timeout=30000) as response_info:
                response = response_info.value
                json_data = response.json()
                browser.close()
                return json_data.get("download_link")
        except Exception as e:
            print(f"Error occurred: {e}")
            if 'browser' in locals():
                browser.close()
            return None

@app.route('/')
def home():
    return "API is running correctly!"

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    terabox_url = data.get('url')
    if not terabox_url:
        return jsonify({"error": "No URL provided"}), 400
        
    mp4_link = get_mp4_link(terabox_url)
    if mp4_link:
        return jsonify({"success": True, "download_link": mp4_link})
    else:
        return jsonify({"error": "Link extraction failed. Server might be busy."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
