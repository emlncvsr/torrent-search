from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    query = data.get('query')
    pages = data.get('pages')
    scraper = data.get('scraper')
    if scraper == 'nyaa':
        result = subprocess.run(['python', 'nyaa_scraper.py', query, str(pages)], capture_output=True, text=True)
    elif scraper == '1337x':
        result = subprocess.run(['python', '1337x.py', query, str(pages)], capture_output=True, text=True)
    else:
        return jsonify({"error": "Invalid scraper specified"}), 400
    return jsonify({"output": result.stdout, "error": result.stderr})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
