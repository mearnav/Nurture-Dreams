from flask import Flask, request, jsonify
from auth import signup_user, login_user
from tracker import log_activity, update_last_action_end
from database import init_db
from auth import get_user_id_by_username

app = Flask(__name__)

init_db()

@app.route("/logs/<int:user_id>", methods=["GET"])
def get_user_logs(user_id):
    from tracker import fetch_logs_for_user
    logs = fetch_logs_for_user(user_id)
    return jsonify(logs)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    result = signup_user(data)
    return jsonify(result)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    result = login_user(data)
    if result['success']:
        log_activity(result['user_id'], 'login', 'User logged in')
    return jsonify(result)

@app.route("/action", methods=["POST"])
def track_action():
    data = request.json
    user_id = data.get("user_id")
    action = data.get("action")
    details = data.get("details")
    log_activity(user_id, action, details)
    return jsonify({"message": "Action logged successfully"})

@app.route("/end_action", methods=["POST"])
def end_action():
    data = request.json
    user_id = data.get("user_id")
    update_last_action_end(user_id)
    return jsonify({"message": "Action end time recorded"})

@app.route("/report", methods=["GET"])
def full_user_report():
    username = request.args.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    from tracker import get_full_user_report
    report = get_full_user_report(username)
    if not report:
        return jsonify({"error": "User not found"}), 404

    return jsonify(report)

if __name__ == "__main__":
    app.run(debug=True)