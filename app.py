from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
import flask
import os
from werkzeug.utils import secure_filename
from service.face_report import faceReport
import datetime
import random
import time
import os
import sys
# BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(BASE_DIR)
sys.path.insert(0, BASE_DIR)

app = flask.Flask(__name__)
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'}

# 判断允许传照片的格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class pic_str:
    def create_uuid(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        randomNum = random.randint(0,100)
        if randomNum <= 10:
            randomNum = str(0)+str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)
        return uniqueNum

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('up.html')

# 上传图片
@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        try:
            user_input = request.form.get("name")
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_dir = os.path.join(BASE_DIR, app.config['UPLOAD_FOLDER'])
                if not os.path.exists(file_dir):
                    os.makedirs(file_dir)
                file.save(os.path.join(file_dir, filename))

                face_report = faceReport(os.path.join(file_dir, filename))
                face_report.save_img()
                face_report.get_proportion()
                data = face_report.get_data()
                del face_report
                import gc
                gc.collect()
                return render_template('up_ok.html', userinput=user_input, imgPath='upload/'+filename, userdata=data)
        except:
            return flask.jsonify({"message":"not detect human face"})
    return flask.jsonify({'code':0})


# 显示图片
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(BASE_DIR, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

# 下载图片
@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload', filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, threaded=True, debug=True)
