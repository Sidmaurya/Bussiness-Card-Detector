
from flask import Flask, render_template, request,session
import os
import io
import numpy as np
#import cv2
#from werkzeug import secure_filename
import  base64, io
import requests,json
from PIL import Image
import uuid

from flask_autoindex import AutoIndex

app = Flask(__name__)

files_index = AutoIndex(app, os.path.curdir + '/../backend/', add_url_rules=False)
# Custom indexing
@app.route('/media')
@app.route('/media/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)

from werkzeug.utils import secure_filename

app.config['UPLOAD_IMAGE'] = os.path.curdir + '/../backend/images/'


app.secret_key = os.urandom(24)

app.config["IMAGE_UPLOADS"] = "static/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

@app.route("/result",methods=['POST','GET'])
def result():
    data=session['data']
    #session.clear()
    print(request.data)
    return render_template("result.html",data=data)


@app.route("/wait", methods=['POST','GET'])
def wait(path='.'):
    if request.method == 'POST':

        photo = request.files.get('file')
        #img=Image.open(photo)
        img_name=str(uuid.uuid4()).split("-")[0]

        file_ex = '.'+secure_filename(photo.filename).split('.')[-1]
        photo.save(os.path.join(app.config['UPLOAD_IMAGE'],img_name+file_ex ))
        #photo = base64.b64encode(photo.read())
        #photo = photo.decode('utf-8')
        #data = {"img": photo}
        #data=json.dumps(data)
        #r = requests.post(url='http://127.0.0.1:5000/', data=data)
        #print(type(r))
        #print(r)
        #predicting image
        res ={'bussiness_card':'http://127.0.0.1:8181/media/out_image/'+img_name+file_ex,'text_data':'http://127.0.0.1:8181/media/out_text/'+img_name+'.txt'}
        data={"data":res}
        session['data']=data
        return render_template('wait.html')
    else:
        return render_template('result.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181,debug=True)
    