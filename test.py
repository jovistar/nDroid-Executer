#!/usr/bin/python

from ndecom import NdeCom


ndeCom = NdeCom('127.0.0.1', 12325)
retCode = ndeCom.create('./s.apk')
print retCode
