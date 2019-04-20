from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from PIL import Image
from dot import *
from upload_picture import *
 
from datetime import timedelta

app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/angle', methods=['POST', 'GET'])  # 添加路由
def angle():
    if request.method == 'POST':
        color=request.form.get('color')
        #if not color:
            #return jsonify({"error": 1001, "msg": "请选择一个颜色计算网目角度"})
        angle=request.form.get('angle')
        angle=float(angle)
        if color=="c":
            img_angle=Image.open('static/images/img_c_binary.jpg')
            img_angle.save('static/images/img_angle.jpg')
        if color=="m":
            img_angle=Image.open('static/images/img_m_binary.jpg')
            img_angle.save('static/images/img_angle.jpg')
        if color=="y":
            img_angle=Image.open('static/images/img_y_binary.jpg')
            img_angle.save('static/images/img_angle.jpg')
        if color=="k":
            img_angle=Image.open('static/images/img_k_binary.jpg')
            img_angle.save('static/images/img_angle.jpg')
        img=Image.open('static/images/img_angle.jpg')
        img_angle=draw(img,angle)
        img_angle.save('static/images/img_angle_find.jpg')

        return render_template('angle_ok.html',val1=time.time())
 
    return render_template('angle.html')

 

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)
