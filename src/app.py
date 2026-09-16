import os
import sys

# Ajusta sys.path para importações relativas a partir da pasta src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from infrastructure.database import init_db
from Routes.routes import api

app = Flask(__name__)
app.register_blueprint(api)

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)