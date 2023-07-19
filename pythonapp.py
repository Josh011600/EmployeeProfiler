from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user;")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
