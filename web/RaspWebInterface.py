import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request
import datetime

app=Flask(__name__)
    
@app.route('/')
def index():
    now=datetime.datetime.now()
    timeString=now.strftime("%Y-%m-%d %H:%M")
    data=[]
    templateData={
        'title':'Raspberry Pi 3B+ Web Controller',
        'time':timeString,
        'data':data,
    }
    return render_template('index.html',**templateData)

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'/home/calvin/App/__CONTENT/01/{f.filename}')
        return render_template("index.html")

if __name__=='__main__':
    os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/
