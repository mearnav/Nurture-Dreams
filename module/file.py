from flask import Flask, request, jsonify
import os
import pandas as pd

app = Flask(__name__)

@app.route('/readfile', methods=['POST'])
def read_file():
    data = request.get_json()
    file_path = data.get('file_path')

    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400

    if not os.path.exists(file_path):
        return jsonify({'error': f'File not found at path: {file_path}'}), 404

    try:
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            result = df.to_dict(orient='records')  
            return jsonify({'type': 'excel', 'rows': result}), 200

        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                content = f.read()
            return jsonify({'type': 'text', 'content': content}), 200

        else:
            return jsonify({'error': 'Unsupported file type. Only .txt, .xls, .xlsx allowed.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)