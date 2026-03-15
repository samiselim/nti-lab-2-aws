"""
AWS DevOps Lab - Flask Web Application
=======================================
A simple Flask web app that displays a personalized greeting.
Students will containerize this app and deploy it to AWS EC2.
"""

from flask import Flask, render_template
import os
import socket
from datetime import datetime

app = Flask(__name__)

# ============================================================
# STUDENT: Change STUDENT_NAME to your own name!
# ============================================================
STUDENT_NAME = os.environ.get("STUDENT_NAME", "Your Name Here")


@app.route("/")
def home():
    """Main page - displays the student greeting."""
    return render_template(
        "index.html",
        student_name=STUDENT_NAME,
        hostname=socket.gethostname(),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/health")
def health():
    """Health check endpoint - useful for monitoring."""
    return {"status": "healthy", "student": STUDENT_NAME}, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
