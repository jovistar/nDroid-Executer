#!/usr/bin/python

from twisted.internet.protocol import DatagramProtocol
from ndlcom import NdlCom
from Queue import Queue
import threading
from scheduler import Scheduler
from msgmanager import MsgManager
import ndutil
import os
from ndscom import NdsCom
from ndacom import NdaCom
import shutil

class NetManager(DatagramProtocol):
	def setNdlCom(self, ndlCom):
		self.ndlCom = ndlCom
		self.msgManager = MsgManager()
		self.ndsCom = NdsCom('127.0.0.1', 12321)
		self.ndaCom = NdaCom('127.0.0.1', 12323)

	def setNsQueue(self, nsQueue, nsLock):
		self.nsQueue = nsQueue
		self.nsLock = nsLock

	def datagramReceived(self, data, (host, port)):
		self.ndlCom.doCom('Request from %s:%d' % (host, port))
		self.dispatch(data, host, port)

	def dispatch(self, data, host, port):
		retCode, result = self.msgManager.resRequest(data)
		if retCode != 0:
			self.ndlCom.doCom('Error Request')
		else:
			responseData = {}
			if result['request'] == 'create':
				self.ndlCom.doCom('Request: CREATE')
				if not os.path.isfile(result['path']):
					responseData['response'] = 1
				else:
					#FIXME
					retCode, uid = self.ndsCom.create(result['path'])
					if retCode != 0:
						responseData['response'] = 1
					else:
						retCode, path = self.ndsCom.get(uid)
						retCode = self.ndaCom.create(uid, 'u')
						responseData['response'] = 0

						self.nsLock.acquire()
						self.nsQueue.put((path, uid), 1)
						self.nsLock.release()

			msg = self.msgManager.genResponse(responseData)
			self.transport.write(msg, (host, port))
