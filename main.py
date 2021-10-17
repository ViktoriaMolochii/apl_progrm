from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/api/v1/hello-world-6")
    def hello_world():
        return "<p>Hello World 6</p>"

    @app.route("/api/v1/hello-world")
    def hello_world2():
        return "<p>Hello World</p>"

    return app

# .venv\Scripts\activate
# waitress-serve --host 127.0.0.1 --port=5000 --call "main:create_app"
# /api/v1/hello-world-6
# /api/v1/hello-world

# curl -v -XGET http://localhost:5000/api/v1/hello-world-6
