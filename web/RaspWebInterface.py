import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import RPi.GPIO as GPIO
from flask import Flask, flash, render_template, Response, request, redirect, url_for
from dotenv import load_dotenv
from pathlib import Path
from yt_dlp import YoutubeDL

dotenv_path = Path(f'/home/calvin/App/.env')
load_dotenv(dotenv_path=dotenv_path)

APP_PATH = os.getenv('APP_PATH')
BANKS_PATH = os.getenv('BANKS_PATH')
BANK_COUNT = os.getenv('BANK_COUNT')
BANK_SIZE = os.getenv('BANK_SIZE')

app=Flask(__name__)

def sanitize_clip_name(unsanitized):
    return unsanitized.replace('\'','').replace('__', '_').replace('\/', '').replace('\\', '')

def bank_path(bankIndex):
    paddedBankIndex = str(bankIndex).zfill(2)
    return f'{BANKS_PATH}/{paddedBankIndex}'

def clip_path(bankIndex, clipIndex):
    paddedClipIndex = str(clipIndex).zfill(2)

    bDir = Path(bank_path(bankIndex))

    fileNames = sorted([file.name for file in bDir.iterdir() if file.name.startswith(f'{paddedClipIndex}__')]) 
    return f'{bank_path(bankIndex)}/{fileNames[0]}'

def clip_name(bankIndex, clipIndex):
    paddedClipIndex = str(clipIndex).zfill(2)

    bDir = Path(bank_path(bankIndex))

    fileNames = sorted([file.name for file in bDir.iterdir() if file.name.startswith(f'{paddedClipIndex}__')]) 
    return fileNames[0]

def allowed_file(filename):
    return Path(filename).suffix == '.mp4'

def get_bank_size(index):
    bpath = bank_path(index)
    bank_files = [f for f in listdir(bpath) if isfile(join(bpath, f))]
    return len(bank_files)

def is_bank_full(index):
    bank_size = get_bank_size(index)
    return bank_size == BANK_SIZE

@app.route('/')
def index():
    banks = []
    bank_sizes = []

    for bank_index in range(1, int(BANK_COUNT) + 1):
        bpath = bank_path(bank_index)
        bank_files = sorted([f for f in listdir(bpath) if isfile(join(bpath, f))])
        bank_sizes.append(len(bank_files))
        banks.append(bank_files)

    return render_template('index.html', banks=banks, bank_sizes=bank_sizes)

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
                    bank_size = get_bank_size(bank_index)
                    p = f'{bank_path(bank_index)}/{str(bank_size+1).zfill(2)}__{sanitize_clip_name(f.filename)}'
                    f.save(p)

        return redirect(url_for('index'))

@app.route('/addFromYoutube', methods = ['POST'])
def addFromYoutube():
    if request.method == 'POST':
        form_data = request.form
        link = form_data.get('link')
        bankIndex = form_data.get('bank')
        bank_size = get_bank_size(bankIndex)

        # the options for this object are in the README of the library
        # but all the examples are fro invoking via command line,
        # where the arg names are all a little differents sometimes.
        # Took me a while to find the proper key to match the cli `-o` output flag
        # but I found it here
        # https://github.com/yt-dlp/yt-dlp/blob/0b6f829b1dfda15d3c1d7d1fbe4ea6102c26dd24/yt_dlp/YoutubeDL.py#L167
        # in the YoutubeDL class source (it was outtmpl)
        yt_opts = {
            'format-sort': 'codec:h264',
            'verbose': True,
            'paths': { 'home': f'{bank_path(bankIndex)}/' },
            'outtmpl': { 'default': f'{str(bank_size+1).zfill(2)}__%(title)s.%(ext)s' }
        }

        with YoutubeDL(yt_opts) as ydl:
            ydl.download(link)

        return redirect(url_for('index'))

@app.route('/rename', methods = ['POST'])
def rename():
    if request.method == 'POST':
        form_data = request.form

        newName = form_data.get('new-name')

        bIndex = int(form_data.get('bank-index'))
        cIndex = int(form_data.get('clip-index'))
        bpath = bank_path(bIndex)
        vpath = clip_path(bIndex, cIndex)

        os.rename(vpath, f'{bpath}/{str(cIndex).zfill(2)}__{newName}');

        return redirect(url_for('index'))

@app.route('/moveup', methods = ['POST'])
def moveup():
    if request.method == 'POST':
        form_data = request.form

        bIndex = int(form_data.get('bank-index'))
        cIndex = int(form_data.get('clip-index'))
        bpath = bank_path(bIndex)
        filename_moving_up = clip_name(bIndex, cIndex)
        filename_moving_down = clip_name(bIndex, cIndex - 1)

        new_filename_moving_up = f"{str(cIndex - 1).zfill(2)}__{filename_moving_up.split(f'{str(cIndex).zfill(2)}__')[1]}"
        new_filename_moving_down = f"{str(cIndex).zfill(2)}__{filename_moving_down.split(f'{str(cIndex - 1).zfill(2)}__')[1]}"

        os.rename(f'{bpath}/{filename_moving_up}', f'{bpath}/{new_filename_moving_up}')
        os.rename(f'{bpath}/{filename_moving_down}', f'{bpath}/{new_filename_moving_down}')

        return redirect(url_for('index'))

@app.route('/movedown', methods = ['POST'])
def movedown():
    if request.method == 'POST':
        form_data = request.form

        bIndex = int(form_data.get('bank-index'))
        cIndex = int(form_data.get('clip-index'))
        bpath = bank_path(bIndex)
        filename_moving_down = clip_name(bIndex, cIndex)
        filename_moving_up = clip_name(bIndex, cIndex + 1)

        new_filename_moving_down = f"{str(cIndex + 1).zfill(2)}__{filename_moving_down.split(f'{str(cIndex).zfill(2)}__')[1]}"
        new_filename_moving_up = f"{str(cIndex).zfill(2)}__{filename_moving_up.split(f'{str(cIndex + 1).zfill(2)}__')[1]}"

        os.rename(f'{bpath}/{filename_moving_up}', f'{bpath}/{new_filename_moving_up}')
        os.rename(f'{bpath}/{filename_moving_down}', f'{bpath}/{new_filename_moving_down}')

        return redirect(url_for('index'))

@app.route('/delete', methods = ['POST'])
def delete():
    if request.method == 'POST':
        form_data = request.form
        fileName = form_data.get('file')
        bankIndex = form_data.get('bank')
        os.remove(f'{bank_path(bankIndex)}/{fileName}')
        return redirect(url_for('index'))

if __name__=='__main__':
    app.secret_key = os.getenv('WEB_APP_SECRET_KEY')
    os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True)
