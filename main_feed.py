from flask import Blueprint, render_template, abort, jsonify
from flask import session as flask_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from jinja2 import TemplateNotFound
from db.setup import Images

engine = create_engine("sqlite:///db/Images.db")

main_feed = Blueprint("main_feed", __name__, template_folder = "templates", static_folder = "static")

# Define limit variable to denote the number of images loaded, ie 5 = 5 images to load
# This will be used for the infinite scroll
num_images = 5

@main_feed.route("/")
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
        
        # A new session will have to be created in every function
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Run a query to get the last 5 uploaded images (as determined by ID #)
        # Increase the count by 1
        q = session.query(Images).order_by(Images.id.desc()).limit(num_images)

        return render_template("index.html", logged_in = logged_in, query = q)
    except TemplateNotFound:
        abort(404)
        
@main_feed.route("/loadcontent/<int:count>", methods = ["GET"])
def loadContent(count):
        
        # A new session will have to be created in every function
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # run the query to get the data. Done same as the initial load, but adds an offset to get 
        # values within a certain range
        # Also, increase the count by 1
        q = session.query(Images).order_by(Images.id.desc()).offset(count*num_images).limit(num_images)
        
        # If the query has no results, return a JSON-ified dictionary with the single entry
        if q.count() == 0:
            return jsonify({"NONE": "0"})
            
        # Construct a dictionary from the query
        return_dict = {}
        for i in range(q.count()):
            return_dict["title" + str(i)] = q[i].title
            return_dict["image_path" + str(i)] = q[i].image_path
            return_dict["caption" + str(i)] = q[i].caption
        
        # Return the JSON to the webpage
        return jsonify(return_dict)
        
        
        