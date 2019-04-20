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

@app.route('/lpi', methods=['POST', 'GET'])  # 添加路由
def lpi():
	if request.method == 'POST':
		color=request.form.get("color")
 
		#if not color:
			#return jsonify({"error": 1001, "msg": "请选择一个效果较好的二值图片计算网目线数"})
		lpi=0
		if color=="c":
			img_lpi=Image.open('static/images/img_c_binary.jpg')
			img_lpi.save('static/images/img_lpi.jpg')
		if color=="m":
			img_lpi=Image.open('static/images/img_m_binary.jpg')
			img_lpi.save('static/images/img_lpi.jpg')
		if color=="y":
			img_lpi=Image.open('static/images/img_y_binary.jpg')
			img_lpi.save('static/images/img_lpi.jpg')
		if color=="k":
			img_lpi=Image.open('static/images/img_k_binary.jpg')
			img_lpi.save('static/images/img_lpi.jpg')
		x1=request.form.get("x1")
		y1=request.form.get("y1")
		x2=request.form.get("x2")
		y2=request.form.get("y2")
		if x1 and y1 and x2 and y2:
			x1=float(x1)
			y1=float(y1)
			x2=float(x2)
			y2=float(y2)
			img=Image.open('static/images/img_lpi.jpg')
			img_rgb=img.convert("RGB")
			img_lpi=drawrect(img_rgb,x1,y1,x2,y2)
			img_lpi.save('static/images/img_lpi_find.jpg')
			img_lpi_cut=cut(img,x1,y1,x2,y2)
			img_lpi_cut.save('static/images/img_lpi_cut.jpg')

			ok=request.form.get("ok")
			if ok=="y":
				img=Image.open('static/images/img.jpg')
				img_binary=Image.open('static/images/img_lpi.jpg')
				img_dot=Image.open('static/images/img_lpi_cut.jpg')
				lpi=calculate_lpi(img,img_binary,img_dot)

		return render_template('lpi_ok.html',lpi=lpi,val1=time.time())

	return render_template('lpi.html')

if __name__ == '__main__':
	# app.debug = True
	app.run(host='0.0.0.0', port=8987, debug=True)
