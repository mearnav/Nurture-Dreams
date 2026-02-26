import sqlite3

# Connect to new DB file
conn = sqlite3.connect("Student_Marks_Dataset.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS marks (
    roll INTEGER,
    name TEXT,
    subject TEXT,
    marks INTEGER
)
''')

# Sample data: 10 students, 6 subjects each
data = [
    (101, 'Arnav', 'Math', 89), (101, 'Arnav', 'Science', 92), (101, 'Arnav', 'English', 85),
    (101, 'Arnav', 'History', 76), (101, 'Arnav', 'Geography', 81), (101, 'Arnav', 'Computer', 94),
    (102, 'Roy', 'Math', 72), (102, 'Roy', 'Science', 68), (102, 'Roy', 'English', 79),
    (102, 'Roy', 'History', 64), (102, 'Roy', 'Geography', 71), (102, 'Roy', 'Computer', 88),
    (103, 'Vaishnavi', 'Math', 91), (103, 'Vaishnavi', 'Science', 89), (103, 'Vaishnavi', 'English', 87),
    (103, 'Vaishnavi', 'History', 90), (103, 'Vaishnavi', 'Geography', 93), (103, 'Vaishnavi', 'Computer', 95),
    (104, 'Raj', 'Math', 66), (104, 'Raj', 'Science', 61), (104, 'Raj', 'English', 70),
    (104, 'Raj', 'History', 60), (104, 'Raj', 'Geography', 65), (104, 'Raj', 'Computer', 74),
    (105, 'Diya', 'Math', 88), (105, 'Diya', 'Science', 91), (105, 'Diya', 'English', 86),
    (105, 'Diya', 'History', 84), (105, 'Diya', 'Geography', 89), (105, 'Diya', 'Computer', 90),
    (106, 'Karan', 'Math', 58), (106, 'Karan', 'Science', 62), (106, 'Karan', 'English', 60),
    (106, 'Karan', 'History', 59), (106, 'Karan', 'Geography', 63), (106, 'Karan', 'Computer', 69),
    (107, 'Ayesha', 'Math', 95), (107, 'Ayesha', 'Science', 94), (107, 'Ayesha', 'English', 97),
    (107, 'Ayesha', 'History', 96), (107, 'Ayesha', 'Geography', 93), (107, 'Ayesha', 'Computer', 98),
    (108, 'Manav', 'Math', 77), (108, 'Manav', 'Science', 73), (108, 'Manav', 'English', 75),
    (108, 'Manav', 'History', 72), (108, 'Manav', 'Geography', 74), (108, 'Manav', 'Computer', 79),
    (109, 'Sneha', 'Math', 84), (109, 'Sneha', 'Science', 86), (109, 'Sneha', 'English', 88),
    (109, 'Sneha', 'History', 85), (109, 'Sneha', 'Geography', 87), (109, 'Sneha', 'Computer', 90),
    (110, 'Aman', 'Math', 69), (110, 'Aman', 'Science', 72), (110, 'Aman', 'English', 74),
    (110, 'Aman', 'History', 70), (110, 'Aman', 'Geography', 73), (110, 'Aman', 'Computer', 76)
]

cursor.executemany("INSERT INTO marks (roll, name, subject, marks) VALUES (?, ?, ?, ?)", data)
conn.commit()
conn.close()

print("✅ student_marks_dataset.db created successfully with sample data.")