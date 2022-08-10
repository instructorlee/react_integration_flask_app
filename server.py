from app import app
import os
from dotenv import load_dotenv
from flask_cors import CORS


CORS(app, support_credentials=True)
app.secret_key = "abcdabcdabcdabcdabcdabcdabcdabcdabcd"

# config
basedir = os.path.abspath(os.path.dirname(__file__))

if 'FLASK_ENV' not in os.environ or os.environ['FLASK_ENV'] == 'development':
    load_dotenv(os.path.join(basedir, 'app/config/development.env'), override=True)
elif os.os.environ['FLASK_ENV'] == 'testing':
    load_dotenv(os.path.join(basedir, 'app/config/testing.env'), override=True)
else:
    load_dotenv(os.path.join(basedir, 'app/config/deployed.env'), override=True)

from app.controllers import user_controller
from app.controllers import topic_controller
from app.controllers import joke_controller

if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True) 