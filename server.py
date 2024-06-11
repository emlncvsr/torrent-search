from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    query = data.get('query')
    pages = data.get('pages')
    scraper = data.get('scraper')

    # Préparation de la requête API vers GitHub Actions
    headers = {
        'Authorization': f'Bearer {os.environ["GH_TOKEN"]}',
        'Accept': 'application/vnd.github.v3+json'
    }
    payload = {
        'ref': 'main',
        'inputs': {
            'query': query,
            'pages': pages,
            'scraper': scraper
        }
    }
    response = requests.post(
        'https://api.github.com/repos/emlncvsr/torrent-search/actions/workflows/scrape.yml/dispatches',
        headers=headers,
        json=payload
    )

    if response.status_code == 204:
        return jsonify({"message": "Scrape initiated, check GitHub Actions for progress."}), 200
    else:
        return jsonify({"message": response.json().get('message')}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)
