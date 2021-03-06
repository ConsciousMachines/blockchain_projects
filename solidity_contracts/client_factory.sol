pragma solidity ^0.4.11;

contract Member {
	// bytes32 instead of strings to use ==; proxies for accounts
    bytes32 public person;
    address private factory;
    uint public points;
	string public description;

	// Constructor
    function Member(bytes32 _person) {
        person = _person;
        factory = msg.sender;
		points = 10; // Beginner Bonus
		description = "New Member! :)";
    }

	// used to verify the transaction sender
    modifier memberActvity(bytes32 _caller) {
        require(msg.sender == factory);
		require(_caller == person);
        _;
    }

	event pointsIncrease(bytes32 a_member, uint pointsChange);

	event pointsDecrease(bytes32 a_member, uint pointsChange);

	event descriptionUpdate(bytes32 a_member, string new_description);

    function pointsBoost(bytes32 memberr, uint boost) public memberActvity(memberr) {
       points += boost;
	   pointsIncrease( memberr, boost);
    }

    function pointsSpend(bytes32 memberr, uint spendAmt) public memberActvity(memberr) {
       points -= spendAmt;
	   pointsDecrease( memberr, spendAmt);
    }

	function modifyDescription(bytes32 memberr, string _description) public memberActvity(memberr) {
       description = _description;
	   descriptionUpdate( memberr, _description);
    }

	// Internal
	function stringToBytes32(string memory source) returns (bytes32 result) {
		bytes memory tempEmptyStringTest = bytes(source);
	    if (tempEmptyStringTest.length == 0) {
	        return 0x0;
	    }
    	assembly {
        	result := mload(add(source, 32))
    	}
	}

	// Non-transaction requiring functons
	// TODO: add an event that shows who looked when calling these from a non-factory address
    function showPoints() constant returns (uint) {
       return points;
    }

	function showDescription() constant returns (bytes32) {
       return stringToBytes32( description );
    }

}
// Council is a factory for generating individuals' amounts
contract Council {

    mapping(bytes32 => address) pointsJournal;

	function newMember(bytes32 memberName) public {
        if (! memberCheck(memberName)) {
            pointsJournal[memberName] = new Member(memberName);
        }
    }

    function pointsBoost(bytes32 memberName, uint boostAmt) public {
        require ( memberCheck(memberName) );
        Member(pointsJournal[memberName]).pointsBoost(memberName, boostAmt);
    }

	function pointsSpend(bytes32 memberName, uint spendAmt) public {
        require ( memberCheck(memberName) );
        Member(pointsJournal[memberName]).pointsSpend(memberName, spendAmt);
    }

	function updateDescription(bytes32 memberName, string newDescription) public {
        require ( memberCheck(memberName) );
        Member(pointsJournal[memberName]).modifyDescription(memberName, newDescription);
    }

	// Internal Functions
	function bytes32ToString(bytes32 x) constant returns (string) {
    	bytes memory bytesString = new bytes(32);
	    uint charCount = 0;
	    for (uint j = 0; j < 32; j++) {
	        byte char = byte(bytes32(uint(x) * 2 ** (8 * j)));
	        if (char != 0) {
	            bytesString[charCount] = char;
	            charCount++;
	        }
	    }
    	bytes memory bytesStringTrimmed = new bytes(charCount);
    	for (j = 0; j < charCount; j++) {
        	bytesStringTrimmed[j] = bytesString[j];
    	}
    	return string(bytesStringTrimmed);
	}

	function memberCheck(bytes32 _memberName) returns (bool) {
		if (pointsJournal[_memberName] != 0) {
			return true;
		}
	}

	// Non-Transaction (Read-Only) Functions
    function showPoints(bytes32 _memberName) public constant returns (uint) {
        if (memberCheck(_memberName)==true){
            return (Member(pointsJournal[_memberName]).showPoints());
        }
	}

	function showDescription(bytes32 _memberName) public constant returns (string) {
		if (memberCheck(_memberName)==true){
	        return (bytes32ToString(Member(pointsJournal[_memberName]).showDescription()));
		}
	}
}
