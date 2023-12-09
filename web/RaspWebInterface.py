import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import RPi.GPIO as GPIO
from flask import Flask, flash, render_template, Response, request
from dotenv import load_dotenv
from pathlib import Path

APP_PATH = '/home/calvin/App'
BANKS_PATH = f'{APP_PATH}/__CONTENT'

dotenv_path = Path(f'{APP_PATH}/.env')
load_dotenv(dotenv_path=dotenv_path)

app=Flask(__name__)

def bank_path(index):
    paddedIndex = str(index).zfill(2)
    return f'{BANKS_PATH}/{paddedIndex}';

def allowed_file(filename):
    return Path(filename).suffix == '.mp4'

@app.route('/')
def index():
    bank_path_1 = bank_path(1)
    onlyfiles = [f for f in listdir(bank_path_1) if isfile(join(bank_path_1, f))]
    return render_template('index.html', files=onlyfiles)

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        else:
            f = request.files['file']

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if f.filename == '':
                return 'No selected file'
            else:
                if f and allowed_file(f.filename):
                    f.save(f'{bank_path(1)}/{f.filename}')
                else:
                    return f'only .mp4 h264 files allowed {f.filename}'

        return index()

@app.route('/delete', methods = ['POST'])
def delete():
    if request.method == 'POST':
        form_data = request.form
        fileName = form_data.get('file')
        os.remove(f'{bank_path(1)}/{fileName}')
        return index()

if __name__=='__main__':
    app.secret_key = os.getenv('WEB_APP_SECRET_KEY')
    os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True)
