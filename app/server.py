# app/server.py
""" Long-running server, implements auth + send message functionalities."""

from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from app.auth import AuthManager
from app.messages import MsgManager

app = Flask(__name__)
auth_manager = AuthManager()
msg_manager = MsgManager(auth_manager)

def check_and_refresh_token():
    """Attempts to refresh token if expired."""

    if auth_manager.is_token_expired() and not auth_manager.renew_token():
        # TODO: Potential error message - Confirm
        return jsonify({"error":{"message":"Failed to refresh token","status":401}})

    return jsonify()

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_and_refresh_token, trigger="interval", minutes=5)
scheduler.start()

# TODO: Confirm what the URL endpoint here should be - test with glific frontend.
@app.route('/login', methods=['POST'])
def login():
    """Create a new session for an existing user."""

    if auth_manager.login():
        return jsonify({'message': 'Login successful', 'access_token': auth_manager.access_token})

    return jsonify({"error":{"message":"Invalid phone or password","status":401}})

@app.route('/send_message/<int:contact_id>', methods=['POST'])
def send_message(contact_id):
    """Creates and sends message."""

    check_and_refresh_token()

    message = request.json.get('message')

    # TODO: Dummy return values for now
    if msg_manager.send_message(contact_id, message):
        return jsonify({'message': 'Send successful', "status":200})

    return jsonify({"error":{"message":"Unable to send message","status":401}})

if __name__ == '__main__':
    app.run(debug=True)
