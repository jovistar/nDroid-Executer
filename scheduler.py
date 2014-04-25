#!/usr/bin/python

import json
import threading
from Queue import Queue
from ndlcom import NdlCom
from ndccom import NdcCom
from ndacom import NdaCom
import time

class Scheduler(threading.Thread):
	def __init__(self, paras, name):
		super(Scheduler, self).__init__()
		self.ndlCom = paras[0]
		self.nsQueue = paras[1]
		self.nsLock = paras[2]
		self.ndcCom = NdcCom('127.0.0.1', 12324)
		self.ndaCom = NdaCom('127.0.0.1', 12323)
		self.name = name

	def run(self):
		self.ndlCom.doCom('%s Started' % self.name)

		while True:
			tmp = self.nsQueue.get(1)
			itemPath = tmp[0]
			itemUid = tmp[1]

			retCode, result = self.ndcCom.scan(itemPath)
			if retCode == 1:
				self.ndlCom.doCom('Scan ERROR')
				self.nsLock.acquire()
				self.nsQueue.put(tmp, 1)
				self.nsLock.release()

			if retCode == 2:
				self.ndlCom.doCom('Scan Queued')
				self.nsLock.acquire()
				self.nsQueue.put(tmp, 1)
				self.nsLock.release()

			if retCode == 0:
				self.ndlCom.doCom('Scan Completed')
				self.ndaCom.update(itemUid, '%d/%d' % (result[1], result[2]))

			time.sleep(30)

