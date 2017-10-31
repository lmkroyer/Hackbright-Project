import textract

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash, 
                   session, url_for, send_from_directory)
from flask_debugtoolbar import DebugToolbarExtension

# from model import User, Rating, Movie, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

UPLOAD_FOLDER = 'filestorage/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def file_to_OCR(file_path):
    """Takes in a file and outputs an OCR'd txt file."""

    # with open(file_path) as ocr_text:

    text = textract.process(file_path)
    return text

@app.route('/')
def index():
    """Homepage."""
  
    return render_template('homepage.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Takes in a document to OCR."""

    if 'file' not in request.files:
        flash('No file part')
        return redirect('homepage.html')
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect('homepage.html')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    #this below part is new, and changed 'filename' to text in 70
    text = file_to_OCR(filename)

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# @app.route('/users')
# def user_list():
#     """Show list of users."""

#     users = User.query.all()
#     return render_template('user_list.html', users=users)

# @app.route('/register')
# def register_user():
#     """Allow user to make an account."""

#     return render_template('registration_form.html')

# @app.route('/registration_confirm', methods=["POST"])
# def redirect_to_users():

#     email = request.form.get("email")
#     password = request.form.get("password")

#     new_user = User(email=email, password=password)
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect("/users")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')