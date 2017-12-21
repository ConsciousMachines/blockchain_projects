from web3 import Web3, HTTPProvider, contract

'''
Simple script for a Clove transaction between two chains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Assumptons:
~~~~~~~~~~~
1. Two blockchains, both connected to via HTTP/RPC

Bob sends B tokens to Clove from his chain, and Clove sends A to Alice's chain.
Bob -> B -> Clove acount on Bob's chain
with a B/C exchange rate or contract,
Clove -> A -> Alice
'''

B = 808 # tokens from Bob
A = 41103 # tokens from Alice

# ACCOUNT SETUP
#~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~

# Bob's address on his chain, and Alice's on hers

bob = '0xe5e57a4069ad2847f7968872fd0bb6e3d0bdf6b1'
alice = '0xb1716e1c4aeeb3bec250e3ebc8d5f2d19defd717'

chain_1_ip = '255.140.22.1'
chain_2_ip = '255.141.22.1'


# connect to chain

# Web3 objects
clove_bob = Web3(HTTPProvider( chain_1_ip )) 
clove_alice = Web3(HTTPProvider( chain_2_ip ))


# addresses
clove_bob_add = clove_bob.personal.listAccounts[0] 
clove_alice_add = clove_alice.personal.listAccounts[0]


# transaction 1: Bob -> Clove
bob2clove = {'from': bob,
       'to' : clove_bob
       'value': B,
       }


# transaction 2: Clove -> Alice
clove2alice = {'from': clove_alice,
       'to' : alice,
       'value': A,
       }


# unlock accounts
clove_bob.personal.unlockAccount( clove_bob_add,'password_bob') 


# send Bob 2 Clove transaction, for which Bob's account 
# must be unlocked on Bob's end.
clove_alice.personal.unlockAccount( clove_alice_add,'password_alice')
clove_bob.eth.sendTransaction( bob2clove )


# optional: wait mining time method here
import time
wait = 0
while clove_bob.eth.getTransactionReceipt( bob2clove ) == None:
    print( 'Waiting for Bob 2 Clove transaction to mine' + wait * '.' )
    wait += 1
    time.sleep(1)


clove_alice.eth.sendTransaction( clove2alice )


a = clove_bob.eth.getTransactionReceipt( bob2clove )
b = clove_alice.eth.getTransactionReceipt( clove2alice )


print( 'Bob 2 Clove Receipt:\n', a )
print( 'Clove 2 Alice Receipt:\n', b )


# TODO: transaction manager
# TODO: verification methods
# TODO: multi-way transactions
# TODO: more complex transactions




