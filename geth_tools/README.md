  # Multichain Setup
  
  The purpose is to set up two private local blockchains using Geth to test chain-to-chain communications and contracts. Here we will use IPC connections. 
  
  After installing [Geth](https://github.com/ethereum/go-ethereum/wiki/Building-Ethereum), dedicate a directory to store your blockchains and nodes. Here we will mark that folder **~** and create the following:
  
  1. Directory to hold chain data, keys, and event log (one per chain) 
  1. Directory for genesis blocks
  
  > NOTE: The setup can get convoluted unless the chain directories are independent. 
  
  A condensed script can be found [here](https://github.com/ConsciousMachines/blockchain_projects/blob/master/geth_tools/bash_commands.txt).
  
  # Setup
  
  The setup can get convoluted unless the chain directories are independent. Here is how we will do it for this example:
  ~~~~~~~~~
  ~ (Main folder)
  |
  |------------------------|-----------------------|-----------------------|-----------------------|
  |                        |                       |                       |                       |
  Genesis Blocks (2)      Chain 1, Node 1         Chain 1, Node 2         Chain 2, Node 1         Chain 2, Node 2
  |                        |
  |-----------|            |-------|----------|
  |           |            |       |          |
  gen1.json   gen2.json    geth    keystore  geth.ipc
  ~~~~~~~~~
  ## Syntax Rules
  * For each chain:
	  * same genesis block
	  * same network ID
	  * nodes connect to each other via admin.addPeer( “<enode_string>“ ) 
  * For each node:
	  * independent directories
	  * different ports
	  * at least one account within each node (admin)
    
  First, we set up the directories in terminal. This can all be done in one terminal window. We set up a chain data directory using a specified genesis block, then create an account. There needs to be at least one account for there to be an admin and perform admin functions such as mining and connecting peer nodes. After you **cd** to your desired directory:
  ~~~~~~~~~
  $ geth --datadir ~/geth_example/chain1node1 init ~/geth_example/gen1.json
  $ geth --datadir ~/geth_example/chain1node2 init ~/geth_example/gen1.json
  $ geth --datadir ~/geth_example/chain2node1 init ~/geth_example/gen2.json
  $ geth --datadir ~/geth_example/chain2node2 init ~/geth_example/gen2.json  
  ~~~~~~~~~
  ## Admin Accounts: 
  ~~~~~~~~~
  $ geth --datadir ~/geth_example/chain1node1 account new
  $ geth --datadir ~/geth_example/chain1node2 account new
  $ geth --datadir ~/geth_example/chain2node1 account new
  $ geth --datadir ~/geth_example/chain2node2 account new
  ~~~~~~~~~
  Next, we need to open 4 terminal windows, 2 will initialize a network and 2 will connect. 
  ~~~~~~~~~
  $ geth --datadir ~/geth_example/chain1node1 --networkid 1111 --port30303 console
  $ geth --datadir ~/geth_example/chain1node2 --networkid 1111 --port30304 console
  $ geth --datadir ~/geth_example/chain2node1 --networkid 2222 --port30305 console
  $ geth --datadir ~/geth_example/chain2node2 --networkid 2222 --port30306 console
  ~~~~~~~~~
  > NOTE: It is possible to write the command:
  ~~~~~~~~~
  $ geth --datadir ~/geth_example/chain1node1 init ~/geth_example/gen1.json --networkid 1111 --port30303 console
  ~~~~~~~~~
  > But this can cause problems in setting up additional nodes. 
  
  This initializes 4 networks total. Instead of this, the second nodes can connect to our primary nodes by:
  ~~~~~~~~~
  $ geth --datadir ~/geth_example/chain1node2 --networkid 1111 --port30304 --bootnodes "<enode>"
  ~~~~~~~~~
  where <enode> is the enode of the first node to initialize the network (chain1node1 and chain2node1 in our example). If these initial nodes already exist, their enode numbers can be found by typing:
  ~~~~~~~~~
  > admin.nodeInfo.enode
  "enode://fa6df19109e3933cc0d5ad7a733da7ee0884be49ed7e6b10cb4567cfbc2d853303e1fb61887e49c5ac37e81816b13d699c6edba4a98c071f8956a0df200ccbe1@[::]:30303"
  ~~~~~~~~~
  into the Javascript console inside the terminal window of the first node. The resulting string is pasted in place of "<enode>" in the above command. For some Mac users this might not work, in which case you can use:
  ~~~~~~~~~  
  > admin.addPeer( "<enode>" )
  ~~~~~~~~~
  to add a peer to your network. Peer can be checked by:
  ~~~~~~~~~
  > admin.peers
  ~~~~~~~~~
  Congratulations! The setup is complete. To check its funcitonality, you can write:
  ~~~~~~~~~
  > miner.start(1) 
  ~~~~~~~~~
  To start mining with 1 thread. Your first two windows will start mining their own blockchain and the other two will mine theirs. This should look something like:
  
![alt text](https://github.com/ConsciousMachines/blockchain_projects/blob/master/geth_tools/mining.png)
  ~~~~~~~~~
  > miner.stop() # to pause mining. 
  ~~~~~~~~~
  
  ## Implementing with Web3-py
  
  When running one chain by itself, using Web3.py to connect is sufficiently easy:
  ~~~~~~~~~
  >>> from web3 import Web3, HTTPProvider, IPCProvider
  >>> web3 = Web3(IPCProvider())
  ~~~~~~~~~
  from there, you can command the chain just like you did from the command line or the Geth Javascript console, for example:
  ~~~~~~~~~
  >>> web3.eth.blockNumber # get current chain block number
  >>> web3.personal.newAccount( "password string" )
  >>> web3.admin.addPeer( "<enode>" )
  >>> web3.miner.start(1)
  >>> web3.miner.stop()
  ~~~~~~~~~
	
  In case this throws an error, your default ipc_path for Web3 is **/Users/yourname/Library/Ethereum/geth.ipc**. If you are running more than 1 chain, you can navigate inside your Python site-packages: 

> ~/site-packages/web3/providers/ipc.py 	

At this stage, if you go back to terminal and **cd** into one of the node folders, for example chain2node2, use the **ls** command to see that the folder contains a hidden element, geth.ipc. There are four of these geth.ipc files since we created 4 nodes. Copy the address of this .ipc file. Navigate into the ipc.py module of Web3, and paste the geth.ipc file address as the **ipc_path** variable on line 23:
 
![alt text](https://github.com/ConsciousMachines/blockchain_projects/blob/master/geth_tools/ipc_path_change.png)
  
  > NOTE: This is a quick workaround for this problem and a thorough solution is coming where you can specify many IPC paths without editing modules.
  
  ## Tools
  
  To connect to a node from a different terminal window, find the geth.ipc file of the desired node, and write in terminal:
  ~~~~~~~~~
  $ geth attach ~/geth_example/chain2node2/geth.ipc
  ~~~~~~~~~
  > NOTE: This is useful in case a terminal window does not initiate in some versions, or is busy mining. 
  
  Set a variable in your bash profile to use as a shortcut for your folder of chains (named eth_chains here. Use the default ethereum folder or your own designated location):
  ~~~~~~~~~
  $ echo ‘export eth_chains=/Users/yourname/ethereum’ >>~/.bash_profile 
  ~~~~~~~~~
  
  ## End 
  
  > Testing done on Geth 1.6, 1.7

  ###### Major differences from earlier versions: 
  * No setSolc (set path to solidity compiler) function after v1.6
  * Differences in including dashes for flags, use -h to list all functions and their options


  ###### Known Issues With Geth
  
  * Command shows no output but goes into the Javascript console: 
   	* Entering the same input will execute it
  * Bootnodes does not work 
    * Use admin.addPeer(*enode*) instead 
  * New genesis block info format (the one in this folder is the latest format)
  * Geth Javascript console does not initiate
	* You can initiate a connection to that node and use the console via *geth attach ipc* (see Tools above)
