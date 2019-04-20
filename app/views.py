from app import app
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
 
#app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/')
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
	if request.method == 'POST':
		f = request.files['file']
 
		if not (f and allowed_file(f.filename)):
			return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
 
		user_input = request.form.get("name")
 
		basepath = os.path.dirname(__file__)  # 当前文件所在路径
 
		upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
		# upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
		f.save(upload_path)
 
		# 使用Opencv转换一下图片格式和名称
		img = cv2.imread(upload_path)
		cv2.imwrite(os.path.join(basepath, 'static/images', 'img.jpg'), img)
		img=Image.open('app/static/images/img.jpg')
		img_cmyk=colorspace(img)
		img_cmyk.save('app/static/images/img_cmyk.jpg')
		img_c,img_m,img_y,img_k=separate(img_cmyk)
		img_c.save('app/static/images/img_c.jpg')
		img_m.save('app/static/images/img_m.jpg')
		img_y.save('app/static/images/img_y.jpg')
		img_k.save('app/static/images/img_k.jpg')
		img_c_binary=binary(img_c,150)
		img_m_binary=binary(img_m,100)
		img_y_binary=binary(img_y,25)
		img_k_binary=binary(img_k,100)
		img_c_binary.save('app/static/images/img_c_binary.jpg')
		img_m_binary.save('app/static/images/img_m_binary.jpg')
		img_y_binary.save('app/static/images/img_y_binary.jpg')
		img_k_binary.save('app/static/images/img_k_binary.jpg')
		#percent_c,percent_m,percent_y,percent_k=calculate(img)
		

		return render_template('upload_ok.html',val1=time.time())
 
	return render_template('upload.html')

@app.route('/upload_ok',methods=['POST','GET'])
def upload_ok():
	return render_template('upload_ok.html')

@app.route('/lpi', methods=['POST', 'GET'])  # 添加路由
def lpi():
	if request.method == 'POST':
		color=request.form.get("color")
 
		#if not color:
			#return jsonify({"error": 1001, "msg": "请选择一个效果较好的二值图片计算网目线数"})
		lpi=0
		if color=="c":
			img_lpi=Image.open('app/static/images/img_c_binary.jpg')
			img_lpi.save('app/static/images/img_lpi.jpg')
		if color=="m":
			img_lpi=Image.open('app/static/images/img_m_binary.jpg')
			img_lpi.save('app/static/images/img_lpi.jpg')
		if color=="y":
			img_lpi=Image.open('app/static/images/img_y_binary.jpg')
			img_lpi.save('app/static/images/img_lpi.jpg')
		if color=="k":
			img_lpi=Image.open('app/static/images/img_k_binary.jpg')
			img_lpi.save('app/static/images/img_lpi.jpg')
		x1=request.form.get("x1")
		y1=request.form.get("y1")
		x2=request.form.get("x2")
		y2=request.form.get("y2")
		if x1 and y1 and x2 and y2:
			x1=float(x1)
			y1=float(y1)
			x2=float(x2)
			y2=float(y2)
			img=Image.open('app/static/images/img_lpi.jpg')
			img_rgb=img.convert("RGB")
			img_lpi=drawrect(img_rgb,x1,y1,x2,y2)
			img_lpi.save('app/static/images/img_lpi_find.jpg')
			img_lpi_cut=cut(img,x1,y1,x2,y2)
			img_lpi_cut.save('app/static/images/img_lpi_cut.jpg')

			ok=request.form.get("ok")
			if ok=="y":
				img=Image.open('app/static/images/img.jpg')
				img_binary=Image.open('app/static/images/img_lpi.jpg')
				img_dot=Image.open('app/static/images/img_lpi_cut.jpg')
				lpi=calculate_lpi(img,img_binary,img_dot)

		return render_template('lpi_ok.html',lpi=lpi,val1=time.time())

	return render_template('lpi.html')

@app.route('/angle', methods=['POST', 'GET'])  # 添加路由
def angle():
	if request.method == 'POST':
		color=request.form.get('color')
		#if not color:
			#return jsonify({"error": 1001, "msg": "请选择一个颜色计算网目角度"})
		if color=="c":
			img_angle=Image.open('app/static/images/img_c_binary.jpg')
			img_angle.save('app/static/images/img_angle.jpg')
		if color=="m":
			img_angle=Image.open('app/static/images/img_m_binary.jpg')
			img_angle.save('app/static/images/img_angle.jpg')
		if color=="y":
			img_angle=Image.open('app/static/images/img_y_binary.jpg')
			img_angle.save('app/static/images/img_angle.jpg')
		if color=="k":
			img_angle=Image.open('app/static/images/img_k_binary.jpg')
			img_angle.save('app/static/images/img_angle.jpg')
		
		angle=request.form.get('angle')
		if angle:
			angle=float(angle)
			img=Image.open('app/static/images/img_angle.jpg')
			img_angle=draw(img,angle)
			img_angle.save('app/static/images/img_angle_find.jpg')

		return render_template('angle_ok.html',val1=time.time())
 
	return render_template('angle.html')

@app.route('/shape', methods=['POST', 'GET'])  # 添加路由
def shape():
	if request.method == 'POST':
		x1=request.form.get("x1")
		y1=request.form.get("y1")
		x2=request.form.get("x2")
		y2=request.form.get("y2")
		if x1 and y1 and x2 and y2:
			x1=float(x1)
			y1=float(y1)
			x2=float(x2)
			y2=float(y2)
			img=Image.open('app/static/images/img_lpi.jpg')
			img_rgb=img.convert("RGB")
			img_lpi=drawrect(img_rgb,x1,y1,x2,y2)
			img_lpi.save('app/static/images/img_lpi_find.jpg')
			img_lpi_cut=cut(img,x1,y1,x2,y2)
			img_lpi_cut.save('app/static/images/img_lpi_cut.jpg')

		dot=request.form.get("dot")
		if dot=="y":
			img_dot=cv2.imread('app/static/images/img_lpi_cut.jpg')
			dot_shape=dotshape(img_dot)
			return render_template('shape_ok.html',dot_shape=dot_shape,val1=time.time())

	return render_template('shape.html')

@app.route('/percentage', methods=['POST', 'GET'])  # 添加路由
def percentage():
	if request.method == 'POST':
		img=Image.open('app/static/images/img.jpg')
		img_c_binary=Image.open('app/static/images/img_c_binary.jpg')
		img_m_binary=Image.open('app/static/images/img_m_binary.jpg')
		img_y_binary=Image.open('app/static/images/img_y_binary.jpg')
		img_k_binary=Image.open('app/static/images/img_k_binary.jpg')
		percent_c,percent_m,percent_y,percent_k=calculate(img,img_c_binary,img_m_binary,img_y_binary,img_k_binary)
		percent_c=int(percent_c*100+0.5)
		percent_m=int(percent_m*100+0.5)
		percent_y=int(percent_y*100+0.5)
		percent_k=int(percent_k*100+0.5)
		return render_template('percentage_ok.html',c=percent_c,m=percent_m,y=percent_y,k=percent_k,val1=time.time())


	return render_template('percentage.html')
