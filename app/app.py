"""A tiny Flask application used to demonstrate a CI/CD pipeline.

The app is deliberately small so the focus stays on the pipeline,
not on the application code. It exposes a few routes and one pure
function (`add`) that is easy to unit test.
"""

from flask import Flask, jsonify

app = Flask(__name__)


def add(a, b):
    """Return the sum of two numbers. Kept pure so it is trivial to test."""
    return a + b


@app.route("/")
def home():
    return jsonify(message="Hello from the CI/CD mini project", status="ok")


@app.route("/health")
def health():
    """Health endpoint. Useful later for deployment readiness checks."""
    return jsonify(status="healthy")


@app.route("/add/<int:a>/<int:b>")
def add_route(a, b):
    return jsonify(result=add(a, b))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
