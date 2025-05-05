from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins (for testing)

# Track connected peers (in production, use a database)
peers = {}

@app.route("/")
def home():
    return "P2P Signaling Server is running!"

@socketio.on("connect")
def handle_connect():
    peer_id = request.sid  # Unique connection ID
    peers[peer_id] = peer_id
    print(f"Peer connected: {peer_id}")
    emit("connected", {"peer_id": peer_id})

@socketio.on("signal")
def handle_signal(data):
    target_peer = data["target_peer"]
    if target_peer in peers:
        emit("signal", data, to=target_peer)  # Relay signals between peers

@socketio.on("disconnect")
def handle_disconnect():
    peer_id = request.sid
    if peer_id in peers:
        del peers[peer_id]
    print(f"Peer disconnected: {peer_id}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
