#!/usr/bin/python
from moneroRPClib import *

rpc = moneroRPClib("127.0.0.1", 18082)
print "Your address:"
print rpc.getaddress()['result']['address']
