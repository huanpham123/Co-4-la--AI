from flask import Flask, render_template, request, jsonify
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Cho phép CORS cho tất cả các nguồn

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Route để render HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route xử lý API request cho câu hỏi văn bản
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')

    if message:
        app.logger.info(f"Received message: {message}")
        api_url = f"https://deku-rest-api.gleeze.com/api/gpt-4o?q={message}&uid=unique_id"
        try:
            response = requests.get(api_url)

            # Log phản hồi từ API
            app.logger.debug(f"API Response: {response.text}")

            # Kiểm tra mã trạng thái phản hồi
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    return jsonify({'reply': response_data.get('result', 'No answer provided')})
                except ValueError:
                    app.logger.error("Invalid JSON response from API.")
                    return jsonify({'error': 'Invalid response from API.', 'details': response.text})
            else:
                app.logger.error(f"API returned an error: {response.status_code} {response.text}")
                return jsonify({'error': f'API error: {response.status_code}'})
        except Exception as e:
            app.logger.error(f"Error occurred while processing request: {str(e)}")
            return jsonify({'error': 'An error occurred while processing your request.'})

    return jsonify({'error': 'No message provided'})

if __name__ == '__main__':
    app.run(debug=True)
