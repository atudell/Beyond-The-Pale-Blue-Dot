from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask import session as flask_session
from jinja2 import TemplateNotFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from datetime import date, datetime
from inputs.validations import Input
from db.setup import Images
import imghdr
import os

upload = Blueprint("upload", __name__, template_folder = "templates", static_folder = "static")

# Assign variables to the root path and the uploads folder, accordingly
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, "static", "uploads")

@upload.route("/upload")
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
    
    # If the user is loged in, go to the uploads template as normal
    if logged_in:
        try:
            return render_template("upload.html", logged_in = logged_in, error = "")
        except TemplateNotFound:
            abort(404)
    # If the user is not logged in, redirect to the login page
    else:
        try:
            return redirect(url_for("login.show"))
        except TemplateNotFound:
            abort(404)     

@upload.route("/upload", methods = ["POST"])       
def uploadImage():

    # Create blank error message
    error = ""

    if request.method == "POST":
        
        # Create new Input objects from the request's form
        title = Input(request.form["txtTitle"])
        caption = Input(request.form["txtCaption"])
        
        # Validate the title and caption data types. If they aren't strings, they'll be converted to strings
        title.checkDataType()
        caption.checkDataType()
        
        # Validate that the title and captions are appropiate lengths. Titles may be up to 50 characters and captions to 100 characters
        # Neither can be left blank. If they aren't correct, it will return to the upload page with an error message.
        # While this is l=already done on the client-side, it will also be done here as well
        if not title.isCorrectLength(1, 50) or not caption.isCorrectLength(1, 100):
            error = "ERROR: Title may not exceed 50 characters. Caption may not exceed 100 characters. Neither may be left blank."
            return render_template("upload.html", error = error)
        
        # Validate that the title and caption do not contain non-ASCII characters. If they do return to the upload page with an error
        if not title.isAscii() or not caption.isAscii():
            error = "ERROR: Non-ASCII characters, such as emojis or other unusual symbols, found"
            return render_template("upload.html", error = error)
        
        # Read the file name as a string
        file = request.files.get("fileUpload", None)
        
        # Validate that there's a file in the request
        if file == None:
            error = "ERROR: No file found"
            return render_template("upload.html", error = error)

        # Validate the file type by actually reading the content of the file
        # Read the first 512 bytes, enough to the find the header
        header = file.read(512)
        # Reset stream
        file.seek(0)
        # Get the format based on the header
        file_type = imghdr.what(None, header)    
        if file_type not in ["jpeg", "jpg", "png", "gif"]:
            error = "ERROR: Only .jpeg, .png, and .gif files permitted"
            return render_template("upload.html", error = error)
        
        
        # Save the file locally
        # The file name will be the username + the date and time of upload to retain uniqueness
        file_name = str(flask_session["user_id"]) + str(datetime.now()).replace(":", "") + "." + file_type       
        file.save(os.path.join(UPLOAD_FOLDER, file_name))
        
    
	    # Create engine by connecting to database
	    engine = create_engine(
            "mysql+pymysql://{username}:{password}@{host}/{database_name}",
            poolclass = NullPool
        )
        
        # A new session will have to be created in every function
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # create a new movie and enter it into the database
        new_image = Images(
                title = title.string, 
                caption = caption.string, 
                image_path = file_name,
                date_created = str(date.today().strftime("%Y/%m/%d")),
                user_id = flask_session["user_id"]
                )
        session.add(new_image)
        session.commit()
        session.close()

        return redirect(url_for("upload.show"))
    
    else:
        return redirect(url_for("upload.show"))
