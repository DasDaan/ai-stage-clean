from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # connects the frontend and backend

# Databaseconfiguration
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="", 
    database="aistage"  
)

@app.route('/api/contact', methods=['POST'])
def save_contact():
    try:
        # gets the data from the contact form
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        message = data.get('message')

        # checks if the fields are empty
        if not first_name or not last_name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400

        # saves the data in the database
        cursor = db.cursor()
        sql = "INSERT INTO ContactMessages (first_name, last_name, email, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (first_name, last_name, email, message))
        db.commit()

        return jsonify({"message": "Contact message saved successfully!"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to save contact message."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)