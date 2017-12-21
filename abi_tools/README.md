# ABI TO STRING AND BACK

Used for encoding the ABI of a smart contract into a string to be sent over ZMQ, and then convert the string back into the ABI file (nested list/ dict data structure). Note: right now it is using everyone's favorite example voting contract from the Remix homepage. We can encode any contract by removing the example code and inserting a sys.arg[1] python call instead. 

~~~~~~
ABI UNFORMATTED:

 [{'stateMutability': 'nonpayable', 'payable': False, 'inputs': [{'type': 'address', 'name': 'to'}], 'type': 'function', 'outputs': [], 'constant': False, 'name': 'delegate'}, {'stateMutability': 'view', 'payable': False, 'inputs': [], 'type': 'function', 'outputs': [{'type': 'uint8', 'name': '_winningProposal'}], 'constant': True, 'name': 'winningProposal'}, {'stateMutability': 'nonpayable', 'payable': False, 'inputs': [{'type': 'address', 'name': 'toVoter'}], 'type': 'function', 'outputs': [], 'constant': False, 'name': 'giveRightToVote'}, {'stateMutability': 'nonpayable', 'payable': False, 'inputs': [{'type': 'uint8', 'name': 'toProposal'}], 'type': 'function', 'outputs': [], 'constant': False, 'name': 'vote'}, {'stateMutability': 'nonpayable', 'type': 'constructor', 'payable': False, 'inputs': [{'type': 'uint8', 'name': '_numProposals'}]}] 

ENCODED ABI: <class 'str'> 

 startlist
    listelement
        startdict
            stateMutability
                nonpayable
            payable
                False
            inputs
                startlist
                    listelement
                        startdict
                            type
                                address
                            name
                                to
                        enddict
                endlist
            type
                function
            outputs
                startlist
                endlist
            constant
                False
            name
                delegate
        enddict
    listelement
        startdict
            stateMutability
                view
            payable
                False
            inputs
                startlist
                endlist
            type
                function
            outputs
                startlist
                    listelement
                        startdict
                            type
                                uint8
                            name
                                _winningProposal
                        enddict
                endlist
            constant
                True
            name
                winningProposal
        enddict
    listelement
        startdict
            stateMutability
                nonpayable
            payable
                False
            inputs
                startlist
                    listelement
                        startdict
                            type
                                address
                            name
                                toVoter
                        enddict
                endlist
            type
                function
            outputs
                startlist
                endlist
            constant
                False
            name
                giveRightToVote
        enddict
    listelement
        startdict
            stateMutability
                nonpayable
            payable
                False
            inputs
                startlist
                    listelement
                        startdict
                            type
                                uint8
                            name
                                toProposal
                        enddict
                endlist
            type
                function
            outputs
                startlist
                endlist
            constant
                False
            name
                vote
        enddict
    listelement
        startdict
            stateMutability
                nonpayable
            type
                constructor
            payable
                False
            inputs
                startlist
                    listelement
                        startdict
                            type
                                uint8
                            name
                                _numProposals
                        enddict
                endlist
        enddict
endlist

DECODED ABI: <class 'list'> 

 [{'type': 'function', 'payable': False, 'inputs': [{'type': 'address', 'name': 'to'}], 'stateMutability': 'nonpayable', 'constant': False, 'outputs': [], 'name': 'delegate'}, {'type': 'function', 'payable': False, 'inputs': [], 'stateMutability': 'view', 'constant': True, 'outputs': [{'type': 'uint8', 'name': '_winningProposal'}], 'name': 'winningProposal'}, {'type': 'function', 'payable': False, 'inputs': [{'type': 'address', 'name': 'toVoter'}], 'stateMutability': 'nonpayable', 'constant': False, 'outputs': [], 'name': 'giveRightToVote'}, {'type': 'function', 'payable': False, 'inputs': [{'type': 'uint8', 'name': 'toProposal'}], 'stateMutability': 'nonpayable', 'constant': False, 'outputs': [], 'name': 'vote'}, {'stateMutability': 'nonpayable', 'type': 'constructor', 'payable': False, 'inputs': [{'type': 'uint8', 'name': '_numProposals'}]}] 

ORIGINAL ABI: <class 'list'> 

 [{'stateMutability': 'nonpayable', 'payable': False, 'inputs': [{'type': 'address', 'name': 'to'}], 'type': 'function', 'outputs': [], 'constant': False, 'name': 'delegate'}, {'stateMutability': 'view', 'payable': False, 'inputs': [], 'type': 'function', 'outputs': [{'type': 'uint8', 'name': '_winningProposal'}], 'constant': True, 'name': 'winningProposal'}, {'stateMutability': 'nonpayable', 'payable': False, 'inputs': [{'type': 'address', 'name': 'toVoter'}], 'type': 'function', 'outputs': [], 'constant': False, 'name': 'giveRightToVote'}, {'stateMutability': 'nonpayable', 'payable': False, 'inputs': [{'type': 'uint8', 'name': 'toProposal'}], 'type': 'function', 'outputs': [], 'constant': False, 'name': 'vote'}, {'stateMutability': 'nonpayable', 'type': 'constructor', 'payable': False, 'inputs': [{'type': 'uint8', 'name': '_numProposals'}]}] 

VARIABLE CHECK: decoded == ab
 True

~~~~~~
