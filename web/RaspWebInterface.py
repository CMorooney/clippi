import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import RPi.GPIO as GPIO
from flask import Flask, flash, render_template, Response, request
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(f'/home/calvin/App/.env')
load_dotenv(dotenv_path=dotenv_path)

APP_PATH = os.getenv('APP_PATH')
BANKS_PATH = os.getenv('BANKS_PATH')
BANK_COUNT = os.getenv('BANK_COUNT')
BANK_SIZE = os.getenv('BANK_SIZE')

app=Flask(__name__)

def bank_path(bankIndex):
    paddedBankIndex = str(bankIndex).zfill(2)
    return f'{BANKS_PATH}/{paddedBankIndex}'

def video_path(bankIndex, videoIndex):
    paddedVideoIndex = str(videoIndex).zfill(2)
    return f'{bank_path(bankIndex)}/{paddedVideoindex}'

def allowed_file(filename):
    return Path(filename).suffix == '.mp4'

def is_bank_full(index):
    bpath = bank_path(index)
    bank_files = [f for f in listdir(bpath) if isfile(join(bpath, f))]
    return len(bank_files) == BANK_SIZE

@app.route('/')
def index():
    banks = []

    for bank_index in range(1, int(BANK_COUNT) + 1):
        bpath = bank_path(bank_index)
        bank_files = [f for f in listdir(bpath) if isfile(join(bpath, f))]
        banks.append(bank_files)

    return render_template('index.html', banks=banks)

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file')
        else:
            f = request.files['file']
            form_data = request.form
            bank_index = form_data.get('bank')

            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if f.filename == '':
                flash('No selected file')
            else:
                if not allowed_file(f.filename):
                    flash(f'only .mp4 h264 files allowed {f.filename})')
                elif is_bank_full(bank_index):
                    flash(f'bank {bank_index} is full (max {BANK_SIZE})')
                else:
                    p = f'{bank_path(bank_index)}/{f.filename}'
                    f.save(p)

        return index()

@app.route('/delete', methods = ['POST'])
def delete():
    if request.method == 'POST':
        form_data = request.form
        fileName = form_data.get('file')
        bankIndex = form_data.get('bank')
        os.remove(f'{bank_path(bankIndex)}/{fileName}')
        return index()

if __name__=='__main__':
    app.secret_key = os.getenv('WEB_APP_SECRET_KEY')
    os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True)
