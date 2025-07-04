# Webhook Receiver App

This Flask application receives GitHub webhook events (push, pull request, merge) from another repository and stores them in MongoDB Atlas. It also displays the latest events on a web interface.

## 🌐 Features

- Receives GitHub webhook events
- Saves event data into MongoDB Atlas
- Displays events in browser with auto-refresh every 15s

## 🚀 Tech Stack

- Python + Flask
- MongoDB Atlas
- HTML (Jinja2)
- Ngrok (for local webhook exposure)

## 📦 Setup Instructions

1. Clone this repo:
   ```bash
   git clone https://github.com/girishpatil28/webhook-repo.git
   cd webhook-repo
# webhook-repo
Flask backend and frontend UI.

pip install -r requirements.txt

python app.py

ngrok http 5000

https://your-ngrok-id.ngrok-free.app/webhook
