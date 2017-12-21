sours = '''
pragma solidity ^0.4.0;
contract Ballot {

    struct Voter {
        uint weight;
        bool voted;
        uint8 vote;
        address delegate;
    }
    struct Proposal {
        uint voteCount;
    }

    address chairperson;
    mapping(address => Voter) voters;
    Proposal[] proposals;

    /// Create a new ballot with $(_numProposals) different proposals.
    function Ballot(uint8 _numProposals) public {
        chairperson = msg.sender;
        voters[chairperson].weight = 1;
        proposals.length = _numProposals;
    }

    /// Give $(toVoter) the right to vote on this ballot.
    /// May only be called by $(chairperson).
    function giveRightToVote(address toVoter) public {
        if (msg.sender != chairperson || voters[toVoter].voted) return;
        voters[toVoter].weight = 1;
    }

    /// Delegate your vote to the voter $(to).
    function delegate(address to) public {
        Voter storage sender = voters[msg.sender]; // assigns reference
        if (sender.voted) return;
        while (voters[to].delegate != address(0) && voters[to].delegate != msg.sender)
            to = voters[to].delegate;
        if (to == msg.sender) return;
        sender.voted = true;
        sender.delegate = to;
        Voter storage delegateTo = voters[to];
        if (delegateTo.voted)
            proposals[delegateTo.vote].voteCount += sender.weight;
        else
            delegateTo.weight += sender.weight;
    }

    /// Give a single vote to proposal $(toProposal).
    function vote(uint8 toProposal) public {
        Voter storage sender = voters[msg.sender];
        if (sender.voted || toProposal >= proposals.length) return;
        sender.voted = true;
        sender.vote = toProposal;
        proposals[toProposal].voteCount += sender.weight;
    }

    function winningProposal() public constant returns (uint8 _winningProposal) {
        uint256 winningVoteCount = 0;
        for (uint8 prop = 0; prop < proposals.length; prop++)
            if (proposals[prop].voteCount > winningVoteCount) {
                winningVoteCount = proposals[prop].voteCount;
                _winningProposal = prop;
            }
    }
}
'''



def true(dic):
    '''The functon for encoding the ABI into a specifically formatted string,
    that is also very readable.'''
    global stringu
    stringu = ''
    def nice(dic,i=0):
        global stringu
        if type(dic)==list:
            stringu+=(i*' '+'startlist\n')
            i += 4
            for k in dic:
                stringu+=(i*' '+'listelement\n')
                nice(k,i=i+4)
            i -= 4
            stringu+=(i*' '+'endlist\n')
        if type(dic)==dict:
            stringu+=(i*' '+'startdict\n')
            i+=4
            for k in dic.keys():
                stringu+=(i*' '+k+'\n')
                nice(dic[k],i=i+4)
            i-=4
            stringu+=(i*' '+'enddict\n')
        elif type(dic) not in (list,dict):
            stringu+=(i*' '+str(dic)+'\n')
    nice(dic)
    return stringu



def abi(i = 0):
    '''Function for decoding the ABI back into the original form'''
    line = yo[i]
    line2 = yo[i+1]
    if line2 == '':
        pass
    a = count_delims(line)
    b = count_delims(line2)
    if b > a:
        if line.strip() == 'startlist':
            l = []
            c = 1
            while count_delims( yo[i+c] ) >= b:
                if count_delims( yo[i+c] ) == b:
                    l.append( abi(i=i+c) )
                c += 1
            return l
        if line.strip() == 'listelement':
            return abi( i=i+1 )
        if line.strip() == 'startdict':
            d = {}
            c = 1
            while count_delims( yo[i+c] ) >= b:
                if count_delims( yo[i+c] ) == b:
                    d[yo[i+c].strip()]=abi( i=i+c+1 )
                c += 1
            return d
        if line.strip() not in ('startlist','listelement','startdict'):
            return abi(i=i+1)
    if b == a: # this only happens for empty lists (see dicts)
        return []
    if b < a:
        if line.strip() == 'True':
            return True
        if line.strip() == 'False':
            return False
        elif line.strip() not in ('True','False'):
            return line.strip()


def count_delims(string, d=' ', t=4):
    i=0
    delim = t*d
    while string[i*t:(i+1)*t] == delim:
        i+=1
    return i






# ACTUAL SCRIPT #
#################


from solc import compile_source

ab = compile_source( sours )['<stdin>:Ballot']['abi']
ayyy = true(ab) # encoded ABI (in string format)
yo = ayyy.split('\n')
decoded = abi()

print('\n\n\nABI UNFORMATTED:\n\n' , ab, '\n')
print('ENCODED ABI:', type(ayyy), '\n\n', ayyy )
print('DECODED ABI:', type(decoded), '\n\n', decoded, '\n')
print('ORIGINAL ABI:',type(ab),'\n\n',ab,'\n')
print('VARIABLE CHECK: decoded == ab\n', decoded == ab )


















