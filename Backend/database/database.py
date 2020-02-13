from redis import Redis
import sys
sys.path.append('../')
from .. import config


class Db(object):
	"""数据库操作类"""
	def __init__(self, opt):
		super(Db, self).__init__()
		self.op_redis0 = Redis(host = opt.host, port = opt.port, db=0, decode_responses=True)
		self.op_redis1 = Redis(host = opt.host, port = opt.port, db=1, decode_responses=True)

	def save_data(self, my_id, my_name, feature):
		"""
		数据入库
		"""
		if self.op_redis0.hexists(my_id, "name"):
			return "-1"
		else:
			self.op_redis0.hset(my_id, "name", my_name)
			self.op_redis0.hset(my_id, "feature", feature)
			self.op_redis1.sadd("id",my_id)
			return "1"


	def get_name(self, my_id):
		"""
		查询用户
		"""
		if self.op_redis0.hexists(my_id, "name"):
			my_name = self.op_redis0.hget(my_id,"name")
			return my_name
		else:
			return "-1"

	def get_feature(self, my_id):
		"""
		查询特征
		"""
		if self.op_redis0.hexists(my_id, "feature"):
			feature = self.op_redis0.hget(my_id,"feature")
			return feature
		return "-1"

	def get_ids(self):
		"""
		查询特征
		"""
		id_set = self.op_redis1.smembers("id")
		return id_set

	def del_data_by_ids(self, id_list):
		"""
		删除
		"""
		res = []
		for my_id in id_list:
			r_num = self.op_redis0.hdel(my_id, "name")
			r_num = self.op_redis0.hdel(my_id, "feature")
			self.op_redis1.srem("id",my_id)
			res.append((my_id, str(r_num)))
		return res

	def del_all_data(self):
		"""
		删除所有数据
		"""
		re_len = self.op_redis1.scard('id')
		tmp = []
		nums = 0
		for _id in self.get_ids():
			tmp.append(_id)
			r_num = self.op_redis0.hdel(_id, "name")
			r_num = self.op_redis0.hdel(_id, "feature")
		for _id in tmp:
			nums += 1
			self.op_redis1.srem("id",_id)

		return re_len == nums, self.op_redis1.scard('id')


if __name__ == "__main__":
	from redis import Redis
	opt = config.opt
	db = Db(opt)
	#res = db.del_data_by_ids(['1','2', '3', '4', '5', '6'])
	res = db.del_all_data()
	print(res)
	#name = op_redis.hget("1","name")
	print('success')