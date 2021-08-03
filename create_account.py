from flask import Blueprint, render_template, abort, request, redirect, url_for
from jinja2 import TemplateNotFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from inputs.validations import Input
from db.setup import Users
from datetime import date

# This is from a separate, custom security module not uploaded to Github for security purposes
from inputs.security import Secure

engine = create_engine("sqlite:///db/Images.db")

create_account = Blueprint("create_account", __name__, template_folder = "templates", static_folder = "static")

# Render the create accounts page
@create_account.route("/createaccount")
def show():
    try:
        return render_template("create.html", error = "")
    except TemplateNotFound:
        abort(404)
        
@create_account.route("/createaccount", methods = ["POST"])
def createAccount():
    
    # Create blank error message
    error = ""

    if request.method == "POST":
        
        # Create new input objects from the form inputs
        n_username = Input(request.form["txtNewUsername"])
        n_password = Input(request.form["txtNewPassword"])
        c_password = Input(request.form["txtConfirmPassword"])
        
        # Perform server side validations of user input
        
        # Validate the data types. If they aren't strings, they'll be converted to strings
        n_username.checkDataType()
        n_password.checkDataType()
        c_password.checkDataType()
        
        # Validate that the username and password is between 1 and 50 characters
        # Since passwords need to match, only the n_password variable will be checked
        if not n_username.isCorrectLength(1, 50) or not n_password.isCorrectLength(1, 50):
            error = "ERROR: Username and password must be at least 1 character and no greater than 50 characters."
            return render_template("create.html", error = error)
        
        # Validate that the username and password do not contain non-ASCII characters.
        if not n_username.isAscii() or not n_password.isAscii():
            error = "ERROR: Non-ASCII characters, such as emojis or other unusual symbols, found"
            return render_template("create.html", error = error)
        
        # Validate that the passwords match
        if n_password.string != c_password.string:
            error = "ERROR: Passwords do not match."
            return render_template("create.html", error = error)
        
        # Once the validations are complete, encrypt the username and password
        
        # Create a pepper to salt and pepper the hash
        # The pepper below is for demonstration, as the version on the live site uses a different,
        # more secure version
        pepper = "EXAMPLE"
        
        # Create a new secure object
        secured = Secure(n_username.string, n_password.string)
        
        # Generate a unique salt
        salt = secured.generateSalt()
        
        # Salt and pepper the username and password
        secured.seasonInputs(salt, pepper)
        
        # Get the encrypted username and password
        secured_inputs = secured.encryptInputs(45)
        
        # Now that the inputs are secured, they may be added to the database
        
        # Generate new User object
        new_user = Users(
                username = secured_inputs[0],
                password = secured_inputs[1],
                salt = salt,
                # Date stored as server's date in YYYY/MM/DD format
                date_created = str(date.today().strftime("%Y/%m/%d"))
                )
        
        # Create a new session
        Session = sessionmaker()
        session = Session(bind = engine)
        
        # Check if the username already exists
        q = session.query(Users).filter_by(username = secured_inputs[0]).all()
        if len(q) > 0:
            error = "ERROR: Username taken by another user"
            session.close()
            return render_template("create.html", error = error)
        
        # Add the new user to the database
        try:
            session.add(new_user)
            session.commit()
            session.close()
        except:
            session.rollback()
            session.close()
            error = "INTERNAL SERVER ERROR: New Account Not Saved"
            return render_template("create.html", error = error)
        
        return render_template("create.html", error = "")
        
    else:
        return redirect(url_for("createaccount.show"))