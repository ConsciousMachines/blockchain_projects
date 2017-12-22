// Simple 2-D Neuron architecture

pragma solidity ^0.4.11;

contract Neuron {

    address owner;
    address factory;
    int bias1 = 1;
	int bias2 = 1;
	int b11 = 1;
	int b21 = 1;
	int b12 = 1;
	int b22 = 1;

	// Use different addresses for different parts of the neural net
    function Neuron(address _owner) {
        owner = _owner;
        factory = msg.sender;
    }

	// Use different modifiers to set where in the neural network the cell is.
    modifier isOwner(address _caller) {
        require(msg.sender == factory);
        require(_caller == owner);
        _;
    }

	function setState(address caller, int _b11, int _b12, int _b21, int _b22, int _bias1, int _bias2) constant isOwner(caller) {
		b11 = _b11;
		b12 = _b12;
		b21 = _b21;
		b22 = _b22;
		bias1 = _bias1;
		bias2 = _bias2;
	}

	function forwardPass(int x1, int x2, int p1, int p2) constant returns (int y1, int y2) {
		return (relu (x1*b11 + x2*b12 + bias1),
			relu (x1*b11 + x2*b12 + bias2));
	}

	function relu(int x) constant returns (int){
		if (x >= 0) {
			return x;
		}
		else {
			return 0;
		}
	}

    function getState() public constant returns (int,int,int,int,int,int) {
       return (b11,b12,b21,b22,bias1,bias2);
    }
}

// Factory to generate many neurons for a neural network
contract NeuronFactory {

    mapping(address => address) cells;

    function createNeuron() public {
        if (cells[msg.sender] == 0) {
            cells[msg.sender] = new Neuron(msg.sender);
        }
    }

	function setState(address caller, int _b11, int _b12, int _b21, int _b22, int _bias1, int _bias2) private constant {
		Neuron(cells[msg.sender]).setState(caller, _b11,_b12, _b21, _b22, _bias1, _bias2);
	}

	function forwardPass(int x1, int x2, int p1, int p2) private constant returns (int y1, int y2) {
		return Neuron(cells[msg.sender]).forwardPass(x1,y2,p1,p2);
	}

	function getState() public constant returns (int,int,int,int,int,int) {
       return Neuron(cells[msg.sender]).getState();
    }
}
