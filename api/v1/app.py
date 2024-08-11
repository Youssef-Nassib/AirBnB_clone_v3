#!/usr/bin/python3
"""let's start a flask application"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)

app.register_blueprint(app_views)

corps = CORS(app, origins="0.0.0.0")

@app.teardown_appcontext
def appTeardown(error):
    """ Close the Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ show the message not found"""
    return (jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
