# flask app.py
from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # if dockerfile set ENV PORT, get it.
    port = int(os.environ.get('PORT', 5000))
    # dev debug -> True, prod debug --> False
    debug = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug, host='0.0.0.0', port=port)
