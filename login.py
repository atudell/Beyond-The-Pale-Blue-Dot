from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask import session as flask_session
from jinja2 import TemplateNotFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool 
from sqlalchemy import create_engine
from inputs.validations import Input
from db.setup import Users

# This is from a separate, custom security module not uploaded to Github for security purposes
from inputs.security import Secure

login = Blueprint("login", __name__, template_folder = "templates", static_folder = "static")

# Render the create accounts page
@login.route("/login")
def show():
    try:
        return render_template("login.html", error = "")
    except TemplateNotFound:
        abort(404)
        
# log the user in
@login.route("/login", methods = ["POST"])
def loginUser():
    
    # Create blank error message
    error = ""
    
    if request.method == "POST":
        
        # Create new input object from username and password
        username = Input(request.form["txtUsername"])
        password = Input(request.form["txtPassword"])
        
        # The only validation will be to check and convert the data type
        username.checkDataType()
        password.checkDataType()
        
        # Confirm that the inputs are the correct length (especially not blank)
        if not username.isCorrectLength(1, 50) or not password.isCorrectLength(1, 50):
            error = "ERROR: Username and password must be at least 1 character and no greater than 50 characters."
            return render_template("login.html", error = error)
        
        # Use the same pepper as used in the create accounts
        # The pepper below is for demonstration, as the version on the live site uses a different,
        # more secure version
        # The salt is simply a placeholder since its unique for each account and it hasn't been used, yet
        pepper = "EXAMPLE"
        salt = ""
        
        # Create a new Secure object and season the inputs
        # The username will match, but the password will need to be corrected
        secured = Secure(username.string, password.string)
        secured.seasonInputs(salt, pepper)
        
        # Get the encrypted username and password
        secured_inputs = secured.encryptInputs(45)
        
	    engine = create_engine(
            "mysql+pymysql://{username}:{password}@{host}/{database_name}",
            poolclass = NullPool
        )
        
        # Start a new database session
        Session = sessionmaker()
        session = Session(bind = engine)
        
        # Query the database for the username
        q = session.query(Users).filter_by(username = secured_inputs[0]).all()
        if len(q) == 0:
            error = "ERROR: Username not found."
            session.close()
            return render_template("login.html", error = error)
        
        # Re-declare the salt variable to the correct value
        salt = q[0].salt
        
        # Re-encrypt username and password with the proper parameters
        validate = Secure(username.string, password.string)
        validate.seasonInputs(salt, pepper)
        validate_inputs = validate.encryptInputs(45)
        
        # Validate the passwords match
        if q[0].password == validate_inputs[1]:
            # Store the login status in session memory
            flask_session["logged"] = "1"
            # Store the user id in session memory
            flask_session["user_id"] = q[0].id
            
            # Close the session and redirect to the main feed
            session.close()
            return redirect(url_for("main_feed.show"))
        # If the passwords don't match, return the login screen with an error message
        else:
            error = "Password or username doesn't match our records"
            session.close()
            return render_template("login.html", error = error)

# Create a function to log out      
@login.route("/logout")
def logoutUser():    
    
    # Trying to access the flask session with a key that hasn't been set, yet will cause an error
    # So, the session is captured in try/except block
    # If the attempt is successful, it will set the logged_in variable as true, false otherwise
    logged_in = None
    
    try:
        if flask_session["logged"] == "1":
            logged_in = True
    except:
        logged_in = False
    
    # If the user was logged in, set the logged_in variable to false and redirect to login page
    if logged_in:
        logged_in = False
        # Assign any other value other to the logged varariable. In this case 0 for false
        flask_session["logged"] = "0"
        return render_template("login.html", error = "")  
    # If the user was never logged in, simply redirect to the login page, anyway
    else: 
        return render_template("login.html", error = "")  
