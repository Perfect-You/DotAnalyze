from PIL import Image,ImageDraw
import math
import cv2 as cv
import numpy as np

def area(img):#面积计算
	width=img.size[0]
	height=img.size[1]
	S=width*height
	return S,width,height

def karea(img):
	count=0
	
	for i in range(0,img.width):#遍历所有长度的点
		for j in range(0,img.height):#遍历所有宽度的点
			data = (img.getpixel((i,j)))#打印该图片的所有点
			if (data[0]<100 and data[1]<100 and data[2]<100):
				count+=1#统计黑色像色点的数量
	return count

def dotarea(img):
	count=0
	pixels=img.load()
	for i in range(img.width):
		for j in range(img.height):
			if pixels[i,j]<100:
				count+=1
	return count

def colorspace(img):
	img_cmyk=img.convert("CMYK")
	return img_cmyk

def separate(img_cmyk):
	im=img_cmyk
	im=im.split()
	#im[0].show()
	#im[0].save('c.jpg')
	img_c=im[0]
	img_m=im[1]
	img_y=im[2]
	img_k=im[3]
	return img_c,img_m,img_y,img_k

def binary(img,n):
	pixels = img.load()
	for x in range(img.width):
		for y in range(img.height):
			pixels[x, y] = 255 if pixels[x, y] < n else 0#n是阈值
	return img

def percent(s,s1,s2):
	s_view=s-s1
	s_dot=s2-s1
	per=s_dot/s_view
	return per

def calculate(img,img_c_binary,img_m_binary,img_y_binary,img_k_binary):
	#img=Image.open('dot2.jpg')
	s,width,height=area(img)
	s1=karea(img)
	#img_cmyk=colorspace(img)
	#img_c,img_m,img_y,img_k=separate(img_cmyk)
	#img_c_binary=binary(img_c,150)#阈值越小，网点百分比越小
	#img_m_binary=binary(img_m,100)
	#img_y_binary=binary(img_y,25)
	#img_k_binary=binary(img_k,100)
	s2_c=dotarea(img_c_binary)
	s2_m=dotarea(img_m_binary)
	s2_y=dotarea(img_y_binary)
	s2_k=dotarea(img_k_binary)
	percent_c=percent(s,s1,s2_c)
	percent_m=percent(s,s1,s2_m)
	percent_y=percent(s,s1,s2_y)
	percent_k=percent(s,s1,s2_k)+s1/(s-s1)
	return percent_c,percent_m,percent_y,percent_k

def draw(img,n):
	im01=img
	draw=ImageDraw.Draw(im01)
	draw.line([(0,1512),(4031,1512)],fill=255,width=5)
	draw.line([(2016,0),(2016,3023)],fill=255,width=5)
	angle=n
	rad=angle*(math.pi)/180
	h=1512*math.cos(rad)
	w=1512*math.sin(rad)
	draw.line([(2016-h,1512+w),(2016+h,1512-w)],fill=255,width=5)
	return im01

def drawrect(img,x1,y1,x2,y2):
	im01=img
	draw=ImageDraw.Draw(im01)
	draw.rectangle((x1,y1,x2,y2),outline=(255,0,0),width=5)
	return im01

def cut(img,x1,y1,x2,y2):
	im=img
	cropedIm = im.crop((x1, y1, x2, y2))
	return cropedIm

def calculate_lpi(img,img_binary,img_dot):
	s,width,height=area(img)#图片面积
	s_k=karea(img)#图片中黑色边框面积
	s_view=s-s_k#视野部分面积
	l=72#img.info['dpi'][0]
	w=72#img.info['dpi'][1]
	s_view_true=s_view/(l*w*10000)
	s_binary=dotarea(img_binary)
	s_dots=s_binary-s_k
	s_dot=dotarea(img_dot)
	dot_quantity=s_dots/s_dot
	lpi=math.sqrt(dot_quantity/s_view_true)
	return int(lpi+0.5)

def dotshape(img_dot):
	img_midblur=cv.medianBlur(img_dot,31)
	cv.imwrite('app/static/images/dot_mid.jpg',img_midblur)
	image=cv.imread('app/static/images/dot_mid.jpg')
	#cv.imshow('def',image)
	blurred=cv.GaussianBlur(image,(3,3),0)
	gray=cv.cvtColor(blurred,cv.COLOR_RGB2GRAY)
	xgrad=cv.Sobel(gray,cv.CV_16SC1,1,0)
	ygrad=cv.Sobel(gray,cv.CV_16SC1,0,1)
	edge_output=cv.Canny(xgrad,ygrad,50,150)
	#cv.imshow("edge",edge_output)
	cv.imwrite('app/static/images/edge.jpg',edge_output)
	#cv.waitKey(0)
	#cv.destroyAllWindows()
	img_dot=Image.open('app/static/images/dot_mid.jpg')
	s_dot=karea(img_dot)
	img_edge=Image.open('app/static/images/edge.jpg')
	c_dot=img_edge.width*img_edge.height-dotarea(img_edge)
	roundness=4*(math.pi)*s_dot/(c_dot*c_dot)
	if roundness>0.53:
		shape="圆形"
	if roundness<0.53:
		shape="方形"
	return shape
