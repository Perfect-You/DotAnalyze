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

@app.route('/percentage', methods=['POST', 'GET'])  # 添加路由
def percentage():
	if request.method == 'POST':
		img=Image.open('static/images/img.jpg')
		img_c_binary=Image.open('static/images/img_c_binary.jpg')
		img_m_binary=Image.open('static/images/img_m_binary.jpg')
		img_y_binary=Image.open('static/images/img_y_binary.jpg')
		img_k_binary=Image.open('static/images/img_k_binary.jpg')
		percent_c,percent_m,percent_y,percent_k=calculate(img,img_c_binary,img_m_binary,img_y_binary,img_k_binary)
		return render_template('percentage_ok.html',c=percent_c,m=percent_m,y=percent_y,k=percent_k,val1=time.time())


	return render_template('percentage.html')

if __name__ == '__main__':
	# app.debug = True
	app.run(host='0.0.0.0', port=8987, debug=True)
