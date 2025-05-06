from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all CORS (for testing)

# Track connected peers
peers = {}

@app.route("/")
def home():
    return "P2P Signaling Server is running!"

@socketio.on("connect")
def handle_connect():
    peer_id = request.sid
    peers[peer_id] = peer_id
    print(f"Peer connected: {peer_id}")
    emit("connected", {"peer_id": peer_id})

@socketio.on("signal")
def handle_signal(data):
    sender_id = request.sid
    target_peer = data.get("target_peer")

    if target_peer == "broadcast":
        for pid in peers:
            if pid != sender_id:
                emit("signal", data, to=pid)
    elif target_peer in peers:
        emit("signal", data, to=target_peer)

@socketio.on("disconnect")
def handle_disconnect():
    peer_id = request.sid
    if peer_id in peers:
        del peers[peer_id]
    print(f"Peer disconnected: {peer_id}")

# Production-ready server
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)
