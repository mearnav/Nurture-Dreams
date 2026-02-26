from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/student/<int:roll_number>')
def show_student_data(roll_number):
    conn = sqlite3.connect('Student_Marks_Dataset.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM marks WHERE roll = ?", (roll_number,))
    result = cursor.fetchone()

    if result is None:
        return jsonify({"error": f"No student found with roll number {roll_number}"}), 404

    student_name = result[0]

    cursor.execute("SELECT subject, marks FROM marks WHERE roll = ?", (roll_number,))
    records = cursor.fetchall()
    conn.close()

    data = {
        "roll_number": roll_number,
        "name": student_name,
        "marks": [{"subject": subject, "marks": marks} for subject, marks in records]
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)