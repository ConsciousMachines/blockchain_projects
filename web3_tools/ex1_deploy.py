from web3 import Web3, IPCProvider, contract
import time

'''
Example script to deploy a contract using Web3-py format.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Assumptions:
~~~~~~~~~~~~
0. Contract compiled for Python format
1. Local IPC chain
2. Already has 1 admin account
3. Admin has some some ether/wei
'''


# ACCOUNT SETUP
#~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~

# connect to chain
web3 = Web3(IPCProvider()) # web3 is just the object name here, can be Bob or Alice


# create a recipint account
web3.personal.newAccount('password') # enter password


# start mining to get ether and process upcoming transactions
web3.miner.start(1)


# set account addresses to variables
add0 = web3.personal.listAccounts[0] 
add1 = web3.personal.listAccounts[1]


# unlock both accounts (only need to unlock sender)
web3.personal.unlockAccount( add0,'password_0')
web3.personal.unlockAccount( add1,'password_1')
web3.miner.start(1)


# CONTRACT SETUP
#~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~


# contract info
contract_data = {
            'abi':[{"constant":True,"inputs":[],"name":"speak","outputs":[{"name":"itSays","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"newSaying","type":"string"}],"name":"saySomethingElse","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":False,"stateMutability":"nonpayable","type":"constructor"}],
            'code': '6060604052341561000f57600080fd5b5b6040805190810160405280600c81526020017f48656c6c6f20576f726c642100000000000000000000000000000000000000008152506000908051906020019061005b929190610062565b505b610107565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106100a357805160ff19168380011785556100d1565b828001600101855582156100d1579182015b828111156100d05782518255916020019190600101906100b5565b5b5090506100de91906100e2565b5090565b61010491905b808211156101005760008160009055506001016100e8565b5090565b90565b6102fe806101166000396000f30060606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806350d8531514610049578063b07d7e39146100d8575b600080fd5b341561005457600080fd5b61005c61014d565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561009d5780820151818401525b602081019050610081565b50505050905090810190601f1680156100ca5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34156100e357600080fd5b610133600480803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919050506101f6565b604051808215151515815260200191505060405180910390f35b610155610219565b60008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156101eb5780601f106101c0576101008083540402835291602001916101eb565b820191906000526020600020905b8154815290600101906020018083116101ce57829003601f168201915b505050505090505b90565b6000816000908051906020019061020e92919061022d565b50600190505b919050565b602060405190810160405280600081525090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061026e57805160ff191683800117855561029c565b8280016001018555821561029c579182015b8281111561029b578251825591602001919060010190610280565b5b5090506102a991906102ad565b5090565b6102cf91905b808211156102cb5760008160009055506001016102b3565b5090565b905600a165627a7a723058201fb76f3b043d3abc77aa67ed55160489724d71d99493917192b3f8ac06efd9370029',
            'code_runtime': '60606040526000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806350d8531514610049578063b07d7e39146100d8575b600080fd5b341561005457600080fd5b61005c61014d565b6040518080602001828103825283818151815260200191508051906020019080838360005b8381101561009d5780820151818401525b602081019050610081565b50505050905090810190601f1680156100ca5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34156100e357600080fd5b610133600480803590602001908201803590602001908080601f016020809104026020016040519081016040528093929190818152602001838380828437820191505050505050919050506101f6565b604051808215151515815260200191505060405180910390f35b610155610219565b60008054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156101eb5780601f106101c0576101008083540402835291602001916101eb565b820191906000526020600020905b8154815290600101906020018083116101ce57829003601f168201915b505050505090505b90565b6000816000908051906020019061020e92919061022d565b50600190505b919050565b602060405190810160405280600081525090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061026e57805160ff191683800117855561029c565b8280016001018555821561029c579182015b8281111561029b578251825591602001919060010190610280565b5b5090506102a991906102ad565b5090565b6102cf91905b808211156102cb5760008160009055506001016102b3565b5090565b905600a165627a7a723058201fb76f3b043d3abc77aa67ed55160489724d71d99493917192b3f8ac06efd9370029',
            'source': 'pragma solidity ^0.4.6; contract HelloWorld { string saySomething; function HelloWorld() { saySomething = "Hello World!"; } function speak() constant returns(string itSays) { return saySomething; } function saySomethingElse(string newSaying) returns(bool success) { saySomething = newSaying; return true; } }',
        }


# transaction
# NOTE: for deploying a contract, only the 'from' address is needed. 
tran_0 = { 'from' : add0, 
       }


# contract initialization
hello = contract.Contract.factory(web3 = web3,
            contract_name = 'Hello',
            abi= contract_data["abi"],
            bytecode= contract_data["code"],
            bytecode_runtime= contract_data["code_runtime"],
            source= contract_data["source"],
                                )


# deploy
a = hello.deploy(transaction = tran_0) #returns transaction hash


# check whether the transaction went through, returns tx details.
# a = <transaction hash from above>
b = web3.eth.getTransaction( a ) 
print(b)
print(web3.eth.getTransactionReceipt( a ))


# financial transaction
# NOTE: make sure your chain is mining
tran_1 = {'from': add0,
       'to': add1 ,
       'value': 2,
       #'gasPrice':0,
       }


# NOTE: for testing, the gas estimate is calculated by
# the gas minimum and difficulty settings of the genesis block;
# an easy block called 'gen3.json' can be found in /geth_example/genesis/
gastimate = web3.eth.estimateGas( tran_1 )
print( 'Estimated gas price:', gastimate)


# get balance of each account
balance_0 = web3.eth.getBalance( add0 )
balance_1 = web3.eth.getBalance( add1 )
print( 'Account balances:', [balance_0, balance_1] )


if balance_0 <= gastimate:
    print( 'Not enough ETH to cover gas cost' )
    web3.miner.start(1)


a = web3.eth.sendTransaction( tran_1 )


wait = 0
while web3.eth.getTransaction( a ) == None:
    message = 'Waiting for transaction to mine' + wait * '.'
    print(message)
    wait += 1
    time.sleep(1)
print( 'Transaction mined!' )
print( 'Account balances:\n', [balance_0, balance_1] )
    
print( 'Receipt:\n', web3.eth.getTransactionReceipt( a ))
print( 'Transaction:\n', web3.eth.getTransaction( a ))

web3.miner.stop()




source = '''
pragma solidity ^0.4.6;

contract HelloWorld {

    string saySomething;

    function HelloWorld() {
        saySomething = "Hello World!";
    }

    function speak() constant returns(string itSays) {
        return saySomething;
    }

    function saySomethingElse(string newSaying) returns(bool success) {
        saySomething = newSaying;
        return true;
    }

}
'''
# contrat from https://ethereum.stackexchange.com/questions/12348/hello-world-smart-contract-using-browser-solidity
# compiled using browser solidity (Remix)
       







