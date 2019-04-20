# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from PIL import Image
from dot import *

from datetime import timedelta
 
#设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
        #user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
 
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'img.jpg'), img)
        img=Image.open('static/images/img.jpg')
        img_cmyk=colorspace(img)
        img_cmyk.save('static/images/img_cmyk.jpg')
        img_c,img_m,img_y,img_k=separate(img_cmyk)
        img_c.save('static/images/img_c.jpg')
        img_m.save('static/images/img_m.jpg')
        img_y.save('static/images/img_y.jpg')
        img_k.save('static/images/img_k.jpg')
        img_c_binary=binary(img_c,150)
        img_m_binary=binary(img_m,100)
        img_y_binary=binary(img_y,25)
        img_k_binary=binary(img_k,100)
        img_c_binary.save('static/images/img_c_binary.jpg')
        img_m_binary.save('static/images/img_m_binary.jpg')
        img_y_binary.save('static/images/img_y_binary.jpg')
        img_k_binary.save('static/images/img_k_binary.jpg')
        #percent_c,percent_m,percent_y,percent_k=calculate(img)
        

        return render_template('upload_ok.html',val1=time.time())
 
    return render_template('upload.html')
 

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)
