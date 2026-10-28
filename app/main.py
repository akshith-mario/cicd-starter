"""A tiny web API. The app itself is deliberately simple:
the point of this project is the pipeline that tests, builds and deploys it."""
import os
from flask import Flask, jsonify

app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "dev")


@app.get("/")
def home():
    return jsonify(message="Hello from the CI/CD starter!", version=VERSION)


@app.get("/health")
def health():
    # Kubernetes liveness/readiness probes call this
    return jsonify(status="ok")


@app.get("/add/<int:a>/<int:b>")
def add(a, b):
    return jsonify(result=a + b)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
