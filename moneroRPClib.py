#!/usr/bin/python
import urllib2
import json

class moneroRPClib:
    def __init__(self, ip, port):
        self.ip = str(ip)
        self.port = str(port)
        self.rpc_url = "http://"+self.ip+":"+self.port+"/json_rpc"
        
    # base request function
    def request_rpc(self, method, params="\"\""):
        data = '{"jsonrpc":"2.0","id":"rpc","method":"'+method+'","params":'+params+'}'
        return json.loads(urllib2.urlopen(self.rpc_url, data=data).read())
        
    """
    getbalance
	return the wallet's balance
	outputs:
		balance: unsigned int
		unlocked_balance: unsigned int
    """
    def getbalance(self):
        return self.request_rpc("getbalance")
    
    """
    getaddress
	return the wallet's address
	outputs:
		address: string
    """
    def getaddress(self):
        return self.request_rpc("getaddress")
    
    """
    getheight
    returns the current block height
    outputs:
        height: string
    """
    def getheight(self):
        return self.request_rpc("getheight")
        
    """
    transfer
	send monero to a number of recipients
	inputs:
		destinations: array of:
			amount: unsigned int
			address: string
		fee: unsigned int
			ignored, will be automatically calculated
		mixin: unsigned int
			number of outpouts from the blockchain to mix with (0 means no mixing)
		unlock_time: unsigned int
			number of blocks before the monero can be spent (0 to not add a lock)
		payment_id: string
	outputs:
	 tx_hash: array of:
		 string
    """
    def transfer(self, destinations, mixin=3, unlock_time=0, payment_id=""):
        params = '{"destinations":'+destinations+', "mixin":'+mixin+', "unlock_time":'+unlock_time+', "payment_id":"'+payment_id+'"}'
        return self.request_rpc("transfer", params)
        
    """
    transfer_split
	same as transfer, but can split into more than one tx if necessary
	inputs:
		destinations: array of:
			amount: unsigned int
			address: string
		fee: unsigned int
			ignored, will be automatically calculated
		mixin: unsigned int
			number of outpouts from the blockchain to mix with (0 means no mixing)
		unlock_time: unsigned int
			number of blocks before the monero can be spent (0 to not add a lock)
		payment_id: string
		new_algorithm: boolean
			true to use the new transaction construction algorithm, defaults to false
	outputs:
	 tx_hash: array of:
		 string
    """
    def transfer_split(self, destinations, mixin=3, unlock_time=0, payment_id="", new_algorithm=False):
        params = '{"destinations":'+destinations+', "mixin":'+mixin+', "unlock_time":'+unlock_time+', "payment_id":"'+payment_id+'", "new_algorithm":'+new_algorithm+'}'
        return self.request_rpc("transfer_split", params)
        
    """
    sweep_dust
	send all dust outputs back to the wallet's, to make them easier to spend (and mix)
	outputs:
		tx_hash_list: list of:
			string
    """
    def sweep_dust(self):
        return self.request_rpc("sweep_dust")
        
    """
    store
	save the blockchain
    """
    def store(self):
        return self.request_rpc("store")
        
    """
    get_payments
	get a list of incoming payments using a given payment id
	inputs:
		payment_id: string
	outputs:
		payments: list of:
			payment_id: string
			tx_hash: string
			amount: unsigned int
			block_height: unsigned int
			unlock_time: unsigned int
    """
    def get_payments(self, payment_id):
        return self.request_rpc("get_payments", '{"payment_id":"'+payment_id+'"}')
        
    """
    get_bulk_payments
	get a list of incoming payments using a given payment id, or a list of payments ids, from a given height
	inputs:
		payment_ids: array of:
			string
		min_block_height: unsigned int
			the block height at which to start looking for payments
	outputs:
		payments: list of:
			payment_id: string
			tx_hash: string
			amount: unsigned int
			block_height: unsigned int
			unlock_time: unsigned int
    """
    def get_bulk_payments(self, payment_ids, min_block_height):
        params = '{"payment_ids":'+payment_ids+', "min_block_height":'+min_block_height+'}'
        return self.request_rpc("get_bulk_payments", params)
        
    """
    incoming_transfers
	return a list of incoming transfers to the wallet
	inputs:
		transfer_type: string
			"all": all the transfers
			"available": only transfers which are not yet spent
			"unavailable": only transfers which are already spent
	outputs:
		transfers: list of:
			amount: unsigned int
			spent: boolean
			global_index: unsigned int
				mostly internal use, can be ignored by most users
			tx_hash: string
				several incoming transfers may share the same hash if they were in the same transaction
			tx_size: unsigned int
    """
    def incoming_transfers(self, transfer_type="all"):
        return self.request_rpc("incoming_transfers", '{"transfer_type":"'+transfer_type+'"}')
        
    """
    query_key
	return the spend or view private key
	inputs:
		key_type: string
			which key to retrieve:
				"mnemonic": the mnemonic seed (older wallets do not have one)
				"view_key": the view key
	outputs:
		key: string
			the view key will be hex encoded
    """
    def query_key(self, key_type="mnemonic"):
        return self.request_rpc("query_key", '{"key_type":"'+key_type+'"}')
        
    """
    make_integrated_address
	make an integrated address from the wallet address and a payment id
	inputs:
		payment_id: string
			hex encoded; can be empty, in which case a random payment id is generated
	outputs:
		integrated_address: string
    """
    def make_integrated_address(self, payment_id=""):
        return self.request_rpc("make_integrated_address", '{"payment_id":"'+payment_id+'"}')
        
    """
    split_integrated_address
	retrieve the standard address and payment id corresponding to an integrated address
	inputs:
		integrated_address: string
	outputs:
		standard_address: string
		payment: string
			hex encoded
    """
    def split_integrated_address(self, integrated_address):
        return self.request_rpc("split_integrated_address", '{"integrated_address":"'+integrated_address+'"}')
        
    """
    stop_wallet
	stops the wallet, storing the current state
    """
    def stop_wallet(self):
        return self.request_rpc("stop_wallet")

if __name__ == "__main__":
    rpc = moneroRPClib("127.0.0.1", 18082)
    print rpc.getbalance()
    print rpc.getaddress()
    print rpc.getheight()
    print rpc.incoming_transfers()
    print rpc.query_key()
    print rpc.query_key("view_key")
    print rpc.make_integrated_address()
    print rpc.split_integrated_address(rpc.make_integrated_address()['result']['integrated_address'])
