from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
from PIL import Image
from dot import *
 
from datetime import timedelta

app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/shape', methods=['POST', 'GET'])  # 添加路由
def shape():
	if request.method == 'POST':
		dot=request.form.get("dot")
		if dot=="y":
			img_dot=cv2.imread('static/images/img_lpi_cut.jpg')
			dot_shape=dotshape(img_dot)
			return render_template('shape_ok.html',dot_shape=dot_shape,val1=time.time())

	return render_template('shape.html')

if __name__ == '__main__':
	# app.debug = True
	app.run(host='0.0.0.0', port=8987, debug=True)
