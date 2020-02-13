from flask import Flask, escape, url_for, request, render_template,render_template, request, jsonify
import os
from random import *
from flask_cors import CORS
from Backend.models.model import ModelFunc
from Backend import config
# 本地调用和远程调用的引用规则不一样
app = Flask('Finger-Vein-Identification-System')
cors = CORS(app, resources={"/api/*": {"origins": "*"}})
opt = config.opt
model = ModelFunc(opt)
#url = '/home/hza/Finger-Vein-Identification-System/Backend/database/imgs'

@app.route('/api/random')
def random_number():
	response = {
		'randomNumber': randint(1, 100)
	}
	return jsonify(response)



@app.route("/api/register", methods=['POST','get']) # 根据名字来见文件夹
def register():
	"""
	注册
	"""
	if request.method == 'POST':
		my_id = request.values.get('id', None)
		my_name = request.values.get('name', None)
		img_files = request.files.getlist('files', None) # 网上的源码坑人 文件列表应该用getlist
		img_root = os.path.join(opt.img_url, my_id)
		if not os.path.exists(img_root):
			os.makedirs(img_root)
		for img in img_files:
			img_name = img.filename
			img_path = os.path.join(img_root, img_name)
			img.save(img_path)
	# 跑模型
	img_root = os.path.join(opt.img_url, my_id)
	res_num = model.register_func(my_id, my_name, img_root)
	response = {
		'resultNumber': res_num
	}
	return jsonify(response)

@app.route("/api/verification", methods=['POST','get']) # 根据名字来见文件夹
def verification():
	"""
	验证
	"""
	if request.method == 'POST':
		my_id = request.values.get('id', None)
		img_file = request.files.get('files', None) # 网上的源码坑人 文件列表应该用getlist
		img_name = img_file.filename
		img_path = os.path.join(opt.ver_img_url, img_name)
		img_file.save(img_path)
	# 跑模型
	res_num = model.verification_func(my_id, img_path)

	response = {
		'resultNumber': res_num
	}
	return jsonify(response)


@app.route("/api/identification", methods=['POST','get']) # 根据名字来见文件夹
def identification():
	"""
	验证
	"""
	if request.method == 'POST':
		img_file = request.files.get('files', None) # 网上的源码坑人 文件列表应该用getlist
		img_name = img_file.filename
		img_path = os.path.join(opt.iden_img_url, img_name)
		img_file.save(img_path)
	# 跑模型
	res_num = model.identification_func(img_path)

	response = {
		'resultNumber': res_num
	}
	return jsonify(response)

'''
@app.route('/user/<username>')
def profile(username):
	return '{}\'s profile'.format(escape(username))

with app.test_request_context(): # 测试请求URL
	print(url_for('index'))
	print(url_for('login'))
	print(url_for('login', next='/'))
	print(url_for('profile', username='John Doe'))



@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		return do_the_login()
	else:
		return show_the_login_form()



@app.route('/login', methods=['GET', 'POST'])
def login():
	"""
	登录
	"""
	if request.method == 'POST':
		return do_the_login()
	else:
		return show_the_login_form()

@app.route('/m', methods=['GET', 'POST'])
def menu():
	"""
	菜单
	"""
	if request.method == 'POST':
		return do_the_login()
	else:
		return show_the_login_form()
'''


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('test.html', name=name)


@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404 # 定制出错页面

# 注册
# 识别
if __name__ == "__main__":
	pass
  	#app.run(host='0.0.0.0', port=5000, debug=True)