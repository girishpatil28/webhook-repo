from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import certifi

app = Flask(__name__)

# MongoDB connection using certifi
client = MongoClient(
    "mongodb+srv://girishpatilm22:Gp282928@cluster0.uaroppb.mongodb.net/?retryWrites=true&w=majority",
    tls=True,
    tlsCAFile=certifi.where()
)
db = client["github_events"]
collection = db["events"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json
    timestamp = datetime.utcnow()

    if event_type == "push":
        author = payload["pusher"]["name"]
        branch = payload["ref"].split("/")[-1]
        message = f"{author} pushed to {branch} on {timestamp.strftime('%d %B %Y - %I:%M %p UTC')}"
        data = {
            "event_type": "push",
            "author": author,
            "to_branch": branch,
            "timestamp": timestamp,
            "message": message
        }

    elif event_type == "pull_request":
        action = payload["action"]
        author = payload["pull_request"]["user"]["login"]
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]

        if action == "opened":
            message = f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp.strftime('%d %B %Y - %I:%M %p UTC')}"
            data = {
                "event_type": "pull_request",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "message": message
            }
        elif action == "closed" and payload["pull_request"]["merged"]:
            message = f"{author} merged branch {from_branch} to {to_branch} on {timestamp.strftime('%d %B %Y - %I:%M %p UTC')}"
            data = {
                "event_type": "merge",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "message": message
            }
        else:
            return "Ignored", 200

    else:
        return "Ignored", 200

    print("Inserting to MongoDB:", data)
    collection.insert_one(data)
    return "OK", 200

@app.route("/api/events")
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for e in events:
        e["_id"] = str(e["_id"])
        e["timestamp"] = e["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")
    return jsonify(events)

# Use Werkzeug to fix WinError on some systems
if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("localhost", 5000, app, use_reloader=True)
