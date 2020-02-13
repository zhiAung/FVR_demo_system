from flask import Flask, request
from flask.ext.restful import Api, Resource

class ClassName(Resource):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
