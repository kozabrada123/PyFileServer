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

      return f"""
<!doctype html>
<html lang="en">

<head>
    <title>File Uploaded!</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS v5.0.2 -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

</head>

<body>

    <div class="row m-4">
        <div class="d-flex align-items-center justify-content-center">
            <div class="card">
                <img class="card-img-top" src="holder.js/100x180/" alt="">
                <div class="card-body">
                    <h4 class="card-title">File uploaded!</h4>
                    <p class="card-text">File {secure_filename(fi.filename)} was succesfully uploaded!</p>
                    <a name="" id="" class="btn btn-primary" href="/{secure_filename(fi.filename)}" role="button">View File</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JavaScript Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
</body>

</html>
        """

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


    if file.type in ["png", "jpg", "jpeg", "gif", "webp", "txt"]:
        #Send with preview
        try:
            html = f"""
    <!doctype html>
    <html lang="en">
    
    <head>
        <title>{curfile.name}</title>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
        <!-- Bootstrap CSS v5.0.2 -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    
    </head>
    
    <body>
    
        <div class="row m-4">
            <div class="d-flex align-items-center justify-content-center">
                <div class="card m-5">
                    <img class="card-img-top" src="holder.js/100x180/" alt="">
                    <div class="card-body p-1">
                        <h4 class="card-title m-2 p-2">{curfile.name}</h4>
                        <p class="card-text m-2 p-2">Path: {str(curfile.path)}</p>
                        <p class="card-text m-2 p-2">Size: {str(curfile.size)}b</p>
                        <p class="card-text m-2 p-2">Type: {str(curfile.type)}</p>
                        <div class="m-3 p-2">
                            <a name="" id="" class="btn btn-secondary mx-1 p-2" href="/{curfile.name}/preview" role="button">Preview</a>
                            <a name="" id="" class="btn btn-primary mx-1 p-2" href="/{curfile.name}/download" role="button">Download</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    
    
    
        <!-- Bootstrap JavaScript Libraries -->
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
    </body>
    
    </html>
            """

            return html

        except:

            html = f"""
            <p>No file "{fname}" found.
            """

            return html

    else:
        #Send without preview
        try:
            html = f"""
        <!doctype html>
        <html lang="en">

        <head>
            <title>{curfile.name}</title>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS v5.0.2 -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

        </head>

        <body>

            <div class="row m-4">
                <div class="d-flex align-items-center justify-content-center">
                    <div class="card m-5">
                        <img class="card-img-top" src="holder.js/100x180/" alt="">
                        <div class="card-body p-1">
                            <h4 class="card-title m-2 p-2">{curfile.name}</h4>
                            <p class="card-text m-2 p-2">Path: {str(curfile.path)}</p>
                            <p class="card-text m-2 p-2">Size: {str(curfile.size)}b</p>
                            <p class="card-text m-2 p-2">Type: {str(curfile.type)}</p>
                            <a name="" id="" class="btn btn-primary p-2 m-3 p-2" href="/{curfile.name}/download" role="button">Download</a>
                        </div>
                    </div>
                </div>
            </div>



            <!-- Bootstrap JavaScript Libraries -->
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
        </body>

        </html>
                """

            return html

        except:

            html = f"""
                <p>No file "{fname}" found.
                """

            return html

def downloadFile(fname):

    curfile = None

    for file in filesm.files:
        if file.name == fname:
            curfile = file


    try:
        return send_file(curfile.path, as_attachment=True)

    except:

        html = f"""
        <p>No file "{fname}" found.
        """

        return html

def previewFile(fname):

    curfile = None

    for file in filesm.files:
        if file.name == fname:
            curfile = file


    try:
        return send_file(curfile.path)

    except:

        html = f"""
        <p>No file "{fname}" found.
        """

        return html

#Start web server
app.run(host='0.0.0.0',debug=True)


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
