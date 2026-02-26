# Nurture Dreams – Cloud-Based Student Data & Activity Tracking Platform

A scalable backend system built using **Python (Flask)** and **SQL**, deployed on **AWS EC2**, providing secure RESTful APIs for authentication, student data management, activity tracking, and dynamic key-value operations.

This system was designed with modular architecture, parameterized endpoints, and structured logging to support scalable data processing and analytics-ready outputs.

---

# 🚀 Architecture Overview

## Backend Layer
- Python (Flask) REST API
- SQL-based data storage
- Parameterized endpoint structure
- Standardized JSON responses

## Cloud Deployment
- Hosted on AWS EC2
- SSH key-based access control
- Configured Security Groups for controlled API exposure
- IAM-based role configuration

## API Testing
- Fully tested using **Postman**
- Structured JSON payloads
- Environment-based endpoint configuration

---

# 🛠 Tech Stack
- Python 3
- Flask
- SQL / SQLite
- AWS EC2
- IAM & Security Groups
- Postman
- JSON / CSV / Excel Handling

---

## ▶ Running the Application (Local – macOS)

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask openpyxl
python3 app.py
```

## Default local server:
```
http://127.0.0.1:5000
```

---

# 🌐 Cloud Deployment (AWS EC2)
- Launch EC2 instance
- Configure inbound rules (Port 22 for SSH, Port 5000 for API)
- SSH into instance:
```bash
ssh -i key.pem ec2-user@<public-ip>
```
- Install dependencies
- Run:
```bash
python3 app.py
```

---

# 📡 API Documentation

## 🔐 Authentication & Activity APIs

## POST /signup
- Registers a new user.
- Example:
```
POST /signup
```
- Body:
```
{
  "name": "Arnav",
  "email": "arnav@email.com",
  "password": "password123"
}
```

## POST /login
- Authenticates user and starts activity tracking.
```
POST /login
```
- Body:
```
{
  "email": "arnav@email.com",
  "password": "password123"
}
```

## POST /action
- Records user activity start.
```
POST /action
```
- Body: 
```
{
  "user_id": 1,
  "action": "Open Dashboard"
}
```

## POST /end_action
- Marks end of activity and calculates time spent.
```
POST /end_action
```
- Body:
```
{
  "user_id": 1,
  "action": "Open Dashboard"
}
```

## GET /logs/<user_id>
- Returns all logged actions for a specific user.
```
GET /logs/1
```

## GET /report?username=<username>
- Returns full activity report including signup time and time spent.
```
GET /report?username=arnav123
```

# 📚 Student Data APIs

## GET /<column>?params=<value>
- Dynamic student query by column.
```
GET /subject?params=Science
```

## GET /filter?params=<class>_<subject>
- Combined filter for class and subject.
```
GET /filter?params=1_Science
```
- Returns Class 1 Science students.

# 🔑 Key-Value APIs

## GET /kv/<key>
- Returns unique values for a column.
```
GET /kv/subject
```

## POST /kv/<key>
- Adds a new value.
- Body: 
```
{
  "value": "History"
}
```

## GET /kvdoc/<key>
- Returns stored text/document for a key.
```
GET /kvdoc/APP_INTRO
```

## POST /kvdoc/<key>
- Updates or inserts text.
- Body:
```
{
  "set_text": "Welcome to the app!"
}
```

---

# 🧪 Testing with Postman
1.	Create a collection: Nurture Dreams APIs
2.	Set base URL:
	•	Local: http://127.0.0.1:5000
	•	AWS: http://<public-ip>:5000
3.	Use:
	•	POST → Body → Raw → JSON
	•	GET → Direct URL parameters

---

# 📊 Design Highlights
- Modular backend architecture
- Parameterized API endpoints
- Role-ready JSON schema responses
- Activity duration calculation logic
- Extensible key-value storage model
- Cloud deployment ready

---

# 🔮 Future Improvements
- Replace SQLite with AWS RDS
- Implement JWT authentication
- Add Docker containerization
- Deploy behind Nginx + Gunicorn
- Integrate CloudWatch monitoring
- Add rate limiting and API versioning
