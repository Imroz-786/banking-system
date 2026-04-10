import sys
import os

# Ensure the backend directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.app import create_app

if __name__ == '__main__':
    app = create_app()
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    print("Starting Banking System Backend on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=debug)
