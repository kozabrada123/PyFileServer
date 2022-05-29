from flask import Flask, send_file, render_template, request
from markupsafe import escape

from werkzeug.utils import secure_filename

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from file import *
from filemanager import *

#Start file manager
filesm = filemanager()
filesm.refreshFiles()

#Refresh files every hour, just in case since we refresh at upload anyway
scheduler = BackgroundScheduler()
scheduler.add_job(func=filesm.refreshFiles, trigger="interval", minutes=60)
scheduler.start()

#Web code
app = Flask(__name__)

#TESTING SIZE, REPLACE ME!
#2 GB
app.config['MAX_CONTENT_PATH'] = 2147483648

@app.route('/')
def index():
   return render_template("home.html")

@app.route('/upload')
def upload_file():
   return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_a_file():
   if request.method == 'POST':

      fi = request.files['file']
      fi.save("files/" + secure_filename(fi.filename))

      #Refresh files
      filesm.refreshFiles()

      print("Uploaded " + secure_filename(fi.filename))

      return render_template('uploadsucess.html', fi_filename=secure_filename(fi.filename))

@app.route(f"/<filename>")
def file(filename):
    return genFileHtml(filename)


@app.route(f"/<filename>/download")
def download(filename):
    return downloadFile(filename)

@app.route(f"/<filename>/preview")
def preview(filename):
    return previewFile(filename)


def genFileHtml(fname):

    curfile = None

    for file in filesm.files:
        if file.name == fname:
            curfile = file


    #if file.type in ["png", "jpg", "jpeg", "gif", "webp", "txt"]:
        #Send with preview
    try:

        return render_template("file.html", curfile_name = curfile.name, curfile_path = curfile.path, curfile_size = curfile.size, curfile_type = curfile.type)

    except:


        return render_template("404.html")

def downloadFile(fname):

    curfile = None

    for file in filesm.files:
        if file.name == fname:
            curfile = file


    try:
        return send_file(curfile.path, as_attachment=True)

    except:

        return render_template("404.html")

def previewFile(fname):

    curfile = None

    for file in filesm.files:
        if file.name == fname:
            curfile = file


    try:
        return send_file(curfile.path)

    except:

        return render_template("404.html")

#Start web server
app.run(host='0.0.0.0',debug=True)


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
