from flask import Flask, send_file, render_template, request, g
from markupsafe import escape
from cryptography.fernet import Fernet

from werkzeug.utils import secure_filename

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from file import *
from filemanager import *

import config

#Start file manager
filesm = filemanager()
filesm.refreshFiles()

#Refresh files every hour, just in case since we refresh at upload anyway
scheduler = BackgroundScheduler()
scheduler.add_job(func=filesm.refreshFiles, trigger="interval", minutes=60)
scheduler.start()

#Web code
app = Flask(__name__)

#Set max size in b
app.config['MAX_CONTENT_LENGTH'] = config.max_filesize_bytes

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

        if config.random_filenames:
            filename = secure_filename(randomizeName(getType(fi.filename)))

        else:
            filename = secure_filename(fi.filename)

        latestfile = filename
        latestfilen = fi.filename

        if config.encrypt:
            key = Fernet.generate_key()
            setLatest(latestfile, latestfilen, key.decode())

            with open(config.files_path + filename, "w") as file:
                # read all file data
                file_data = fi.stream.read()
                # encrypt data
                f = Fernet(key)
                encrypted_data = f.encrypt(file_data)
                
                # Write to disk
                file.write(encrypted_data.decode())



        else:
            setLatest(latestfile, latestfilen)
            fi.save(config.files_path + filename)

        #Refresh files
        filesm.refreshFiles()

        print("Uploaded " + filename)

        if config.encrypt:
            return render_template('uploadsucess.html', fi_filename=filename, fi_filenamen=latestfilen, key = key.decode())
        else:
            return render_template('uploadsucess.html', fi_filename=filename, fi_filenamen=latestfilen)

@app.route('/uploader/<filename>')
def show_uploaded(filename):
    
    latestfile, latestfilen, key = getLatest()

    setLatest("None", "None", "None")
    
    if filename == "latest":
        return render_template('uploadsucess.html', fi_filename=secure_filename(latestfile), fi_filenamen=latestfilen, key = key)

    return render_template('uploadsucess.html', fi_filename=secure_filename(filename), fi_filenamen=latestfilen, key = key)

@app.route(f"/<filename>")
def file(filename):
    if not config.encrypt:
        return genFileHtml(filename)
    else:
        key = request.args['key']
        return genFileHtml(filename, key)


@app.route(f"/<filename>/download")
def download(filename):
    if not config.encrypt:
        return downloadFile(filename)
    else:
        key = request.args["key"]
        return downloadFile(filename, key)


@app.route(f"/<filename>/preview")
def preview(filename):
    if not config.encrypt:
        return previewFile(filename)
    else:
        key = request.args["key"]
        return previewFile(filename, key)


def genFileHtml(fname, key=None):

    curfile = None

    for file in filesm.files:
        if file.name == fname:
            curfile = file


    #if file.type in ["png", "jpg", "jpeg", "gif", "webp", "txt"]:
        #Send with preview
    try:

        return render_template("file.html", curfile_name = curfile.name, curfile_path = curfile.path, curfile_size = normalizeSize(curfile.size), curfile_type = curfile.type, key = str(key))

    except:

        return render_template("404.html")

def downloadFile(fname, key=None):

    curfile = None

    for file in filesm.files:
        if file.name == fname:
            curfile = file


    if not config.encrypt:
        try:
            return send_file(curfile.path, as_attachment=True)

        except:

            return render_template("404.html")


    else:
        try:
            # Decrypt data
            f = Fernet(key.encode())
            file = open(curfile.path, "r")
            file_data = file.read()
            decrypted = f.decrypt(file_data.encode())


            # Convulted way to add _d before the extension
            # Get the extension
            temp_filename_e = curfile.path.split(".")
            temp_filename_e = "." + temp_filename_e[len(temp_filename_e)-1]

            if temp_filename_e == curfile.path:
                temp_filename_e = ""
            
            # Get the filename before extension
            temp_filename = curfile.path.split("/")
            temp_filename = temp_filename[len(temp_filename)-1].replace(temp_filename_e, "")
            
            # Add _d and then the extension
            temp_filename = temp_filename + "_d" + temp_filename_e
            
            # Save temp file
            temp = open(temp_filename, "w", encoding='latin-1')
            temp.write(decrypted.decode('latin-1'))
            temp.close()

            # Send
            send = send_file(temp_filename, as_attachment=True)

            # Delete temp file
            os.remove(temp_filename)

            return send

        except Exception as e:
            print(e)
            

def previewFile(fname, key=None):

    curfile = None

    for file in filesm.files:
        if file.name == fname:
            curfile = file

    if not config.encrypt:
        try:
            return send_file(curfile.path)

        except:

            return render_template("404.html")

    else:
        try:
            # Decrypt data
            f = Fernet(key.encode())
            file = open(curfile.path, "r")
            file_data = file.read()
            decrypted = f.decrypt(file_data.encode())


            # Convulted way to add _d before the extension
            # Get the extension
            temp_filename_e = curfile.path.split(".")
            temp_filename_e = "." + temp_filename_e[len(temp_filename_e)-1]
            
            # Get the filename before extension
            temp_filename = curfile.path.split("/")
            temp_filename = temp_filename[len(temp_filename)-1].replace(temp_filename_e, "")
            
            # Add _d and then the extension
            temp_filename = temp_filename + "_d" + temp_filename_e
            
            # Save temp file
            temp = open(temp_filename, "w", encoding='latin-1')
            temp.write(decrypted.decode('latin-1'))
            temp.close()

            # Send
            send = send_file(temp_filename)

            # Delete temp file
            os.remove(temp_filename)

            return send

        except Exception as e:
            print(e)

#Start web server
app.run(host='0.0.0.0',debug=True)


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
