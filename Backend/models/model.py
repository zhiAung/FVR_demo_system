import os
import json
import numpy as np
import torch
import time
import sys
sys.path.append('../')
from .. import config
from torch.nn import DataParallel
import random
from ..database import database
from . import multi_task_net
from PIL import Image
import torchvision

class ModelFunc(object):
	"""
	功能主类
	"""
	def __init__(self, opt):
		super(ModelFunc, self).__init__()
		self.opt = opt
		# 加载预训练模型
		model = multi_task_net.MultiTastNet(opt)
		if opt.multi_gpus:
			model = DataParallel(model, device_ids = opt.device_ids)
		model.load_state_dict(torch.load(opt.model_parameters))
		if torch.cuda.is_available():
			model = model.cuda()
		model.eval()
		'''
		self.model = torch.load(opt.model_parameters)
		if opt.multi_gpus:
			self.model = DataParallel(self.model, device_ids = opt.device_ids)
		if torch.cuda.is_available():
			self.model = self.model.cuda()
		self.model.eval()
		'''
		self.model = model
		self.db = database.Db(opt)

		
	def img_preprocess(self, img_file_list_url):
		"""
		图片预处理
		"""
		if os.path.isdir(img_file_list_url):
			img_tensors = []
			img_file_list = os.listdir(img_file_list_url)
			for img_file in img_file_list:
				img_url = os.path.join(img_file_list_url, img_file)
				img = Image.open(img_url)
				im = img.resize((320, 240), Image.ANTIALIAS)
				im = im.convert("RGB")
				img_tensor = torchvision.transforms.ToTensor()(im)
				img_tensor = img_tensor.unsqueeze(0)
				img_tensors.append(img_tensor)
			tensor_data = torch.cat(img_tensors, 0) # 多个tensor合成一个
		elif os.path.isfile(img_file_list_url):
			img = Image.open(img_file_list_url)
			im = img.resize((320, 240), Image.ANTIALIAS)
			im = im.convert("RGB")
			img_tensor = torchvision.transforms.ToTensor()(im)
			tensor_data = img_tensor.unsqueeze(0)
		return tensor_data

	def register_func(self, id, name, img_file_list_url):
		"""
		注册
		args:
			opt:config func
			id：手指唯一id，或者是人唯一id
			name: 用户姓名
			img_file_list：静脉图片文件
		"""
		if self.db.get_name(id) != "-1":
			return "-1" # 该id已存在
		else:
			tensors = self.img_preprocess(img_file_list_url)
			features = self.model(tensors)
			features = features.data.cpu().numpy() # 验证一下输出的形状
			re_features = np.mean(features,axis=0)
			#print(features.shape, re_features.shape)
			re_features_l = re_features.tolist()
			re_features_j = json.dumps(re_features_l)
			res_num = self.db.save_data(id, name, re_features_j)
		return res_num # "1":成功 "-1"：该id已存在
		
		
	def verification_func(self, id, img_file_list_url):
		"""
		验证 1:1
		"""
		name = self.db.get_name(id)
		if name == "-1":
			return "-1" # 该id不存在
		else:
			tensors = self.img_preprocess(img_file_list_url)
			features = self.model(tensors)
			features = features.data.cpu().numpy()[0]
			reg_feature = self.db.get_feature(id)
			reg_feature_l = json.loads(reg_feature)
			reg_feature_a = np.array(reg_feature_l) # 待改
			if reg_feature_a != "-1":
				cos = np.dot(reg_feature_a, features) / (np.linalg.norm(reg_feature_a) * np.linalg.norm(features))
		if cos <= 0.5:
			return "-2" # 验证不成功
		return name


	def identification_func(self, img_file_list_url):
		"""
		识别 1:N
		"""
		tensors = self.img_preprocess(img_file_list_url)
		features = self.model(tensors)
		features = features.data.cpu().numpy()[0]
		max_cos = 0
		id_set = self.db.get_ids()
		for f_id in id_set:
			reg_feature = self.db.get_feature(f_id)
			reg_feature_l = json.loads(reg_feature)
			reg_feature_a = np.array(reg_feature_l) # 待改
			cos = np.dot(reg_feature_a, features) / (np.linalg.norm(reg_feature_a) * np.linalg.norm(features))
			if cos <= 1 and cos >= 0 and cos > max_cos:
				max_cos = cos
				result_id = f_id # 字符串的形式
		if max_cos < 0.5:
			return "-1"
		return result_id


if __name__ == '__main__':
	print('test')