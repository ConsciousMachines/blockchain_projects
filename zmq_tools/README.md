# ZMQ Connection Tools

Use Case:
1. Transmit data between each other similar to a blockchain, using JSON format to work with ZMQ. 
2. Transmit Ethereum contract ABIs using ABI -> string tool

Note: here a miner is nicknamed someone who performs as a data transmitter. 
~~~~~~ 
$ python3.5 ~/data_exchange.py
~~~~~~
Yields the following test output (locahost address in example):
~~~~~~
Bob sent out source code on port 5558
Bob sent out source code on port 5560
Bob sent out source code on port 5562
Received source code from author b'69.69.69.69'
Reached author limit, current roster: ["b'69.69.69.69'"]
Beginning Compilation Process...
Compilation of contract from address b'69.69.69.69' failed
Beginning P2P mining...
Bob sent out source code on port 5558
Bob sent out source code on port 5560
Bob sent out source code on port 5562
Bob sent out source code on port 5558
Bob sent out source code on port 5560
Bob sent out source code on port 5562
~~~~~~
