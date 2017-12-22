# Setting up Python + Geth environment variables to work with building and testing Ethereum contracts

# Run your local chain
# $ geth --datadir ~/geth_example/chain1node1 --networkid 1111 --port 30303 console


from web3 import Web3, IPCProvider, contract
from solc import compile_source

import time

me = Web3(IPCProvider(ipc_path = '/Users/your_name/geth_example/chain1node1/geth.ipc'))

me.personal.listAccounts
me.personal.newAccount()
madd1 = me.personal.listAccounts[0]
madd2 = me.personal.listAccounts[1]
pasw = 'my_password'
me.miner.start(1)
me.eth.getBalance( madd1 )
me.eth.getBalance( madd2 )





def get_balances(add1,add2):
	print('Account 1 Balance:', me.eth.getBalance( add1 ), 'Account 2 Balance:', me.eth.getBalance( add2 ) )


def wait_for_deployment(tx_receipt):
	i = 0
	contract_address = tx_receipt['contractAddress']
	while not contract_address:
		print('Waiting' + '.'*i )
		time.sleep(1)
		i+=1
		contract_address = tx_receipt['contractAddress']
	print("Contract Successfully Mined And Exists on the Chain!")
  print("Contract Address:\n",contract_address)
	return contract_address
  
  
def display(dic,i=0): # basically hand-made pprint, to use for showing ABI components nicely
  if type(dic)==dict:
      for key in dic.keys():
          print(i*' '+key)
          display(dic[key],i=i+4)


def con(source): # all steps in one function: unlock account, deploy contract, show transaction, etc...
  # creates a global variable "hello" tha trefers to the web3 contract factory class. Now need to instantiate it:
	c = compile_source( source )
	global c_name, hello, a, yo1, yo2
	for i in c.keys(): # hack to get contract name automatically. Use only with single contracts!
		c_name = i
	hello = contract.Contract.factory(web3 = me,
	            contract_name = 'Hello',
	            abi = c[c_name]['abi'],
	            bytecode = c[c_name]['bin'],
	            bytecode_runtime = c[c_name]['bin-runtime'])
	me.personal.unlockAccount( madd1, pasw , 0)
	tran_0 = { 'from' : madd1 }
	# a is the transaction receipt
	a = hello.deploy(transaction = tran_0)
	info1 = me.eth.getTransaction( a )
	info2 = me.eth.getTransactionReceipt( a )
	print( 'Transaction:\n\n',me.eth.getTransaction( a ),'\n\n')
	print( 'Transaction Receipt:\n\n',me.eth.getTransaction( a ),'\n\n')
	print('\ntransaction hash:\n\n', a)
	print('\nEXTRA: info1 is Txn, info2 is TxnReceipt\n')



# step by step contract deployment & calling example:
# get / set contract source code
c1 = '\npragma solidity ^0.4.0;\n\ncontract SimpleStorage{\n\tuint storedData;\n\tfunction set( uint x){\n\t\tstoredData = x;\n\t}\n\tfunction get() constant returns (uint retVal){\n\t\treturn storedData;\n\t}\n}'
c = compile_source(c1)
contract_data = c['<stdin>:SimpleStorage']
my_contract = me.eth.contract(
abi=contract_data['abi'],
bytecode=contract_data['bin'],
bytecode_runtime=contract_data['bin-runtime'])
tran_0 = {'from': madd1 }

me.personal.unlockAccount( madd1, pasw , 0)
a = my_contract.deploy(transaction = tran_0) # .deploy() returns contract address 

# NOTE: when you run the above, if you are running a Geth node it should show that it received the transaction (in its own bash window):
# INFO [12-21|18:46:13] Submitted contract creation              fullhash=0x392084d517a79a9f7fc3f03097bccf3fc91f90c217af3db2fc94eca6471d25c7 contract=0x3E4Cb7055E391EAda4cB5e8004c82fa083A574DA

me.eth.getTransaction( a )
tx_receipt = me.eth.getTransactionReceipt( a )
contract_address = tx_receipt['contractAddress']
# NOTE: the above step will return None until the contract is mined. So make sure your chain is mining!
# Optionally use this helper function:
contract_address = wait_for_deployment(tx_receipt)

# Once the contract is mined, we can instantiate it., 
# NOTE: this is where it gets tricky because Web3-py ConciseContract does not work any longer :(
# so we have to expeirment for a bit to get it to work:
contract_instance = me.eth.contract(contract_data['abi'], contract_address)

# Now after all that setup, we can finally interact with the contract!
# With Web3-py, reading contract data can be done by using the .call() method on the contract instance. 
# To change the contract's state, we would need to do a transaction. 
contract_instance.call().get() # returns 0 since all contract variables get initiated as 0 in Solidity
# The contract functionality is very specific to the data provided in the transaction dictionary.
# For instance if you provide a 'to' address, then the .set() call won't go through.

contract_instance.transact(tran_0).set(5) #
# Returns transaction hash: 
# '0x0af122d262c4fc8bf761c48090010a41ebeca5417c67548ea96f5e81cda5aef0'

# Now we can contnuously call:
contract_instance.call().get()
# And once the transaction that changes the state is mined, we will receive the new storedData value.


get_balances(madd1,madd2)
tran_f1 = { 'from': madd1,
	   'to': madd2,
	   'value':123456789000 } # a financial transaction to fund our second account for testing (assuming first is mining and therefore has ether)
me.personal.unlockAccount(madd1, pasw, 0)
me.eth.sendTransaction( tran_f1 )
get_balances(madd1,madd2) # might take longer to adjust balance depending on mining speed


tran_1 = {'from':madd2}
contract_instance.transact(tran_1).set(34)
contract_instance.call().get()










