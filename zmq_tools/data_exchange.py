import zmq
import time
from  multiprocessing import Process

# "miner" here has a different meaning from usual blockchains,
# here it is assumed to be a server subcriber who transmits data

# Format Example
# Replace ABI with ABI -> string tool
data = {'author':'127.0.0.1',
        'source': 'hallo',
        'variations': {
            '0x18239uyehriofeb':{
                'bytecode_runtime':'0x18239sdasdsadadsdad',
                'abi':'this is abi',
                'voters':['miner1']
                  } ,
            '0x98py413uh2reogiu43e':{
                'bytecode_runtime':'0x98pyasdasdsaorqgihejb',
                'abi':'this is another abi',
                'voters':['miner3','miner4'], 
                  } ,
            }
        }


sours = '''
pragma solidity ^0.4.14;
    contract Table {
    address owner;
    function Table() {
        owner = msg.sender;
    }
    
    struct Model {
            string author;
            string title;
            address owner;
    }
    
    mapping (uint => Model) lookup;
    
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
    
    function get(uint id) internal returns (Model bb) {
       return lookup[id];
    }
    
    function set(Model b, uint id) onlyOwner internal returns (Model bb){
       lookup[id] = b;
       return lookup[id];
    }
    
    function get_author(uint id) returns (string a) {
            Model memory m = lookup[id];
            return m.author;
        }
    
    function get_title(uint id) returns (string a) {
            Model memory m = lookup[id];
            return m.title;
        }
    
    function get_owner(uint id) returns (address a) {
            Model memory m = lookup[id];
            return m.owner;
        }
    
}
'''
def encode(data,
           delimiter = '///',
           delimiter2 = '***'):
    string = ''.join( [ 
        data['author'], ' ', delimiter,
        data['source'], delimiter, 
        str(len( data['variations'] )),
        ] ) 
            
    for bytecode in data['variations'].keys():
        mini_string = ''.join( [ 
            delimiter,bytecode,delimiter,
            data['variations'][bytecode]['bytecode_runtime'], delimiter, 
            data['variations'][bytecode]['abi'], delimiter,
            ] )
        
        for j in range(len( data['variations'][bytecode]['voters'] )):
            mini_string += data['variations'][bytecode]['voters'][j]
            mini_string += delimiter2
                 
        string += mini_string
    return string


def decode(data,
           delimiter = '///',
           delimiter2 = '***' ):
    data = data.split( delimiter )
    json_file = { 'author': data[0].strip(),
                  'source': data[1],
                  }
    assert int( data[2] )
    variations = {}
    for i in range(int( data[2] )):
        bytecode = data[ 3 + 4*i ]
        variant = { 'bytecode_runtime': data[ 4 + 4*i ],
                    'abi': data[ 5 + 4*i ],
                    'voters': data[ 6 +4*i ].split( delimiter2 )[:-1]
                    }
        variations[bytecode] = variant
    json_file['variations'] = variations
    return json_file


def nice(dic,i=0):
    if type(dic)==dict:
        for key in dic.keys():
            print(i*' '+key[:50])
            if type(dic[key])!=dict:
                #print((i+4)*' '+str(dic[key]))
                print((i+4)*' '+str(type(dic[key])))
            nice(dic[key],i=i+4)


def voter_checker(my_addr, data): # check if miner's addy in voters list
    contains = False
    i = 0
    while not contains:
        if my_addr in data['variations'][i]['voters']:
            contains = True
        i += 1


        
initial_data = {'author':'127.0.0.1',
                'source': sours,
                }


def bob(ports=[], my_addy = '127.0.0.1'):
    if type(ports) != list:
        ports = [ports]
    if len(ports) == 0:
        ports = ['5556']
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    for port in ports:
        socket.bind("tcp://*:%s" % port)
    for i in range(5):
        msg = my_addy + ' ' + sours
        socket.send_string( msg ) # this holds until someone receives the message
        print( 'Bob sent out source code on port %s' % port)
        time.sleep(1)


def miner_get_source( ports, my_addy = '127.0.0.1', cont_len=3 ):
    context = zmq.Context()
    socket_sub = context.socket(zmq.PULL)
    for port in ports:
        socket_sub.connect ("tcp://localhost:%s" % port )
    sources = []
    authors = []
    while len(authors) < cont_len:
        string = socket_sub.recv()
        name = string.split()[0]
        string = string[ len(name) + 1:]
        if name not in authors:
            authors.append( str(name) )
            sources.append( str(string) )
            print( 'Received source code from author %s' % name )
    print('Reached author limit, current roster: %s' % str(authors) )
    print('Beginning Compilation Process...')
    contracts = []
    for source in sources:
        auth = authors[ sources.index(source) ]
        try:
            contract = second_rate_compiler(source = source)
            contract = generate_consensus_file( auth, source, contract, my_addy)
            contracts.append(contract)
            print('Successfully compiled contract!')
        except:
            print('Compilation of contract from address %s failed' % auth )
    
    print('Beginning P2P mining...')
    start_miner( contracts = contracts, authors = authors)
    return None


def generate_consensus_file(author,source,contract_data,my_addy):
    print('AUTHOR:',author)
    data = {'author': author,
            'source': source,
            'variations':
                { contract_data['code']:
                      {
                      'abi':contract_data['abi'],
                      'bytecode_runtime':contract_data['code_runtime'],
                      'voters':[my_addy]
                      }
                }
            }
    print('\n\n\n')
    nice(data)
    return data


def start_miner(contracts, authors):
    miner_ports = ['5569']#,'5566','5568']

    Process(target= miner_broadcast, args=( miner_ports, contracts )).start()
    Process(target= miner_subscribe, args=( miner_ports, authors )).start() 


def miner_broadcast(ports,contracts,
          duration = 300,
          ):
    if type(ports) != list:
        ports = [ports]
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    for port in ports:
        socket.bind("tcp://*:%s" % port)
    start = time.time()
    while time.time() - start <= duration:
        for i in range(len(contracts)):
            consensus_file = contracts[i]
            #nice(consensus_file)
            #print('YOLOSWAG')
            string = encode( consensus_file )
            socket.send_string( string )
        time.sleep(1)


def miner_subscribe(ports, authors):
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    for port in ports:
        sub.connect ("tcp://localhost:%s" % port)

    # The following allows us to filter for specific authors, but only for one.
    sub.setsockopt_string(zmq.SUBSCRIBE, '')
    while True:
        string = sub.recv()
        print( "Received Contract of length %s!" % str(len(string)) )
        string = decode(string)
        nice(string)
        #TODO:finish the rest here


if __name__ == "__main__":
    source_ports = ['5558','5560','5562'] # push/pull

    miner_addy = '127.0.0.1'
    
    server_push_port = "5558"
    Process(target= bob, args=(source_ports[0],'69.69.69.69')).start()
    Process(target= bob, args=(source_ports[1],'128.0.0.1')).start()
    Process(target= bob, args=(source_ports[2],'255.255.255.0')).start()
    
    Process(target= miner_get_source,args=( source_ports, miner_addy,1)).start()    
   
