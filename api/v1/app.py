#!/usr/bin/python3
"""let's start a flask application"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)
@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


if __name__ == '__main__':
    HOST = getenv('HBNH_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
