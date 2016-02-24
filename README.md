# moneroRPCwrapper
Python wrapper for Monero's simplewallet RPC.

# usage
run simplewallet with rpc bind option: ./simplewallet --rpc-bind-port 18082


then use the class (python code example):

	$ from moneroRPClib import *
	$ rpc = moneroRPClib("127.0.0.1", 18082)
	$ print rpc.getaddress()['result']['address']


All rpc functions return json decoded full response objects.

Full documentation copied from https://getmonero.org/knowledge-base/developer-guides/wallet-rpc, is available in moneroRPClib.py file.