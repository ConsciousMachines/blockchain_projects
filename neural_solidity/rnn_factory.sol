// Architecture of this cell involves three 2x2 matrices. One for the input, one for output, and once they go through RELU they go together through the fourth matrix, which is without a bias, so just a linear combination.

// TODO: way to represent floats as bytes
// TODO: backpropagation contract
// TODO: activations other than relu

pragma solidity ^0.4.11;

contract RNNCell {

    address owner;
    address factory;
	// Internal 2D-State Variables: Wx
    int bias1 = 1;
	int bias2 = 1;
	int b11 = 1;
	int b21 = 1;
	int b12 = 1;
	int b22 = 1;
	// Operation Variables for the preious state
	int cbias1 = 1;
	int cbias2 = 1;
	int c11 = 1;
	int c21 = 1;
	int c12 = 1;
	int c22 = 1;
	// Operations for linear combining output and hidden units
	int d11 = 1;
	int d21 = 1;
	int d12 = 1;
	int d22 = 1;

	// Use different addresses for different parts of the neural net
    function RNNCell(address _owner) {
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

	function setHiddenState(address caller, int _c11, int _c12, int _c21, int _c22, int _cbias1, int _cbias2 ) constant isOwner(caller) {
		c11 = _c11;
		c12 = _c12;
		c21 = _c21;
		c22 = _c22;
		cbias1 = _cbias1;
		cbias2 = _cbias2;
	}

	function setOutputState(address caller, int _d11, int _d12, int _d21, int _d22) constant isOwner(caller) {
		d11 = _d11;
		d12 = _d12;
		d21 = _d21;
		d22 = _d22;
	}
	
	// x1 and x2 are inputs, p1 and p2 are the previous state variables
	function forwardPass(int x1, int x2, int p1, int p2) constant returns (int y1, int y2) {
		int _y1;
		int _y2;
		int _h1;
		int _h2;
		// Matrix Multiplication with a bias and RELU
		_y1 = relu (x1*b11 + x2*b12 + bias1);
		_y2 = relu (x1*b11 + x2*b12 + bias2);
		_h1 = relu (p1*c11 + p2*c12 + cbias1);
		_h2 = relu (p1*c11 + p2*c12 + cbias2);
		// No RELU as we want a greater reach of variable scope for the output.
		return (d11*_y1 + d12*_h1,
			d21*_y2 + d22*_h2);
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

	function getHiddenState() public constant returns (int,int,int,int,int,int) {
       return (c11,c12,c21,c22,cbias1,cbias2);
    }

	function getOutputState() public constant returns (int,int,int,int) {
       return (d11,d12,d21,d22);
    }
}

// Factory to generate RNN cells. Can be used as a hash table of addresses of RNN cells in a neural network architecture
contract RNNFactory {

    mapping(address => address) cells;

    function createRNNCell() public {
        if (cells[msg.sender] == 0) {
            cells[msg.sender] = new RNNCell(msg.sender);
        }
    }

	function setState(address caller, int _b11, int _b12, int _b21, int _b22, int _bias1, int _bias2) private constant {
		RNNCell(cells[msg.sender]).setState(caller, _b11,_b12, _b21, _b22, _bias1, _bias2);
	}

	function setHiddenState(address caller, int _c11, int _c12, int _c21, int _c22, int _cbias1, int _cbias2 ) private constant {
		RNNCell(cells[msg.sender]).setHiddenState(caller, _c11,_c12, _c21, _c22, _cbias1, _cbias2);
	}

	function setOutputState(address caller, int _d11, int _d12, int _d21, int _d22) private constant {
		RNNCell(cells[msg.sender]).setOutputState(caller,_d11,_d12,_d21,_d22);
	}

	function forwardPass(int x1, int x2, int p1, int p2) private constant returns (int y1, int y2) {
		return RNNCell(cells[msg.sender]).forwardPass(x1,y2,p1,p2);
	}

	function getState() public constant returns (int,int,int,int,int,int) {
       return RNNCell(cells[msg.sender]).getState();
    }

	function getHiddenState() public constant returns (int,int,int,int,int,int) {
       return RNNCell(cells[msg.sender]).getHiddenState();
    }

	function getOutputState() public constant returns (int,int,int,int) {
       return RNNCell(cells[msg.sender]).getOutputState();
    }
}
