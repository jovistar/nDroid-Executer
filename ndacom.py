#!/usr/bin/python

import socket
import json
import os

class NdaCom():
	def __init__(self, host, port):
		self.address = (host, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def create(self, uid, res):
		data = {}
		if res not in ['b', 'm', 'u']:
			return 1

		data['request'] = 'create'
		data['uid'] = uid
		data['result'] = res

		result = self.doCom(data)
		if result['response'] != 0:
			return 1
		return 0

	def delete(self, uid):
		data = {}
		data['request'] = 'delete'
		data['uid'] = uid

		result = self.doCom(data)
		if result['response'] != 0:
			return 1
		return 0

	def update(self, uid, res):
		data = {}
		if res not in ['b', 'm', 'u']:
			return 1

		data['request'] = 'update'
		data['uid'] = uid
		data['result'] = res

		result = self.doCom(data)
		if result['response'] != 0:
			return 1
		return 0

	def get(self, uid):
		data = {}

		data['request'] = 'get'
		data['uid'] = uid

		result = self.doCom(data)
		if result['response'] != 0:
			return 1, '', ''
		return 0, result['result'], result['lastop']

	def doCom(self, data):
		msg = json.dumps(data)
		self.s.sendto(msg, self.address)
		result,addr = self.s.recvfrom(4096)

		return json.loads(result)
