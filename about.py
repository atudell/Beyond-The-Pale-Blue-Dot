from flask import Blueprint, render_template, abort
from flask import session as flask_session
from jinja2 import TemplateNotFound

about = Blueprint("about", __name__, template_folder = "templates", static_folder = "static")

@about.route("/about")
def show():
    
    # Trying to access the flask session with a key that hasn't been set, yet will cause an error
    # So, the session is captured in try/except block
    # If the attempt is successful, it will set the logged_in variable as true, false otherwise
    logged_in = None
    
    try:
        if flask_session["logged"] == "1":
            logged_in = True
    except:
        logged_in = False
        
    try:
        return render_template("about.html", logged_in = logged_in)
    except TemplateNotFound:
        abort(404)