# -*- coding: utf-8 -*-
from flask import Flask

# Import individual modules
from create_account import create_account
from main_feed import main_feed
from upload import upload
from login import login
from about import about

# Initialize app and register blueprints
app = Flask(__name__)
app.register_blueprint(create_account)
app.register_blueprint(main_feed)
app.register_blueprint(upload)
app.register_blueprint(login)
app.register_blueprint(about)

# Register a secret key to the app so that it can create session data
# Note the Github version will have an example separate from the actual live version for security purpose
app.secret_key = "FOR_DEMO_USE_ONLY"

# make some additional configurations
# The app will ignore requests larger than 5MB
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
# Only allow these extensions
app.config['UPLOAD_EXTENSIONS'] = [".jpeg", ".jpg", ".png", ".gif"]

if __name__ == "__main__":
    app.run(host = "localhost")
