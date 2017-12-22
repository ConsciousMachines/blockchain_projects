'''
Raw Atomic Swap transaction OP_CODES for the Bitcoin side
'''


def raw_atomic_swap(address1, address2, locktim, secret_hash):
	'''
	Generates raw transaction string for an atomic swap on the Bitcoin blockchain.
	-Address1 is that of the initiator
	-Address2 is of the participator
	'''
	contract = str(0x62)+str(0xa6)
	#TODO: Tipemd160 method
	contract += secret_hash
	contract += str(0x80)+str(0x76)+str(0xa9)
	#TODO: conversion methods for addresses
	contract += address2
	contract += str(0x67)
	#TODO: assert proper format for locktime
	contract += locktime
	contract += str(0xb1)+str(0x75)+str(0x76)+str(0xa9)
	contract += address1
	contract += str(0x68)_str(0x88)+str(0xac)
	return contract
