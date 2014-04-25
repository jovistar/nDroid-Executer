#!/usr/bin/python

from netmanager import NetManager
from cnfmanager import CnfManager
from ndlcom import NdlCom
import ndutil

from Queue import Queue
import threading
from scheduler import Scheduler

from twisted.internet import reactor

def nda_loop():
	ndutil.setTimezone()

	ndlCom = NdlCom('nDroid-Executer', '127.0.0.1', 12322)
	ndlCom.doCom('Initiating')

	ndlCom.doCom('Loading Config')
	cnfManager = CnfManager()
	cnfManager.load('./nde.cnf')
	cnfData = cnfManager.getCnfData()

	nsQueue = Queue()
	nsLock = threading.Lock()

	netManager = NetManager()
	netManager.setNdlCom(ndlCom)
	netManager.setNsQueue(nsQueue, nsLock)

	ndlCom.doCom('Starting Threads')
	scheduler = Scheduler([ndlCom, nsQueue, nsLock], 'Scheduler')

	scheduler.start()

	reactor.listenUDP(cnfData['comPort'], netManager)
	ndlCom.doCom('Listening Com Port')
	reactor.run()

	scheduler.join()

if __name__ == '__main__':
	nda_loop()
