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

	// Non-transaction requiring functons
	// TODO: add an event that shows who looked when calling these from a non-factory address
    function showPoints() constant returns (uint) {
       return points;
    }

	function stringToBytes32(string memory source) returns (bytes32 result) {
		bytes memory tempEmptyStringTest = bytes(source);
	    if (tempEmptyStringTest.length == 0) {
	        return 0x0;
	    }
    	assembly {
        	result := mload(add(source, 32))
    	}
	}

	function showDescription() constant returns (bytes32) {
       return stringToBytes32( description );
    }

}
// Council is a factory for generating individuals' amounts
contract Council {

    mapping(bytes32 => address) pointsJournal;

    function newMember(bytes32 memberName) public {
        if (pointsJournal[memberName] == 0) {
            pointsJournal[memberName] = new Member(memberName);
        }
    }

    function pointsBoost(bytes32 memberName, uint boostAmt) public {
        require (pointsJournal[memberName] != 0);
        Member(pointsJournal[memberName]).pointsBoost(memberName, boostAmt);
    }

	function pointsSpend(bytes32 memberName, uint spendAmt) public {
        require (pointsJournal[memberName] != 0);
        Member(pointsJournal[memberName]).pointsSpend(memberName, spendAmt);
    }

	function updateDescription(bytes32 memberName, string newDescription) public {
        require (pointsJournal[memberName] != 0);
        Member(pointsJournal[memberName]).modifyDescription(memberName, newDescription);
    }

	// Non-Transaction (Read-Only) Functions
    function showPoints(bytes32 _memberName) public constant returns (uint) {
        if (pointsJournal[_memberName] != 0) {
            return (Member(pointsJournal[_memberName]).showPoints());
        }
	}

	function showDescription(bytes32 _memberName) public constant returns (bytes32) {
        return (Member(pointsJournal[_memberName]).showDescription());
	}


}
