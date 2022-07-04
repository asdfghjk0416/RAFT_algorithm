
# Raft Algorithm 
## Overview
It is a distributed consensus algorithm. It aims to solve the issue of how data should be distributed across distributed servers and how they communicate with one another.

Raft works by electing a leader who is then in charge of accepting client requests and relaying that information to other worker server. The leader is chosen by periodic elections between the different servers.


## I. Project Structure
1. **Node** :Raft implementation image is be built from this directory. 
2. **Controller** : Controller is how we will interact with your cluster, it will send out JSON requests to the cluster
   and our implementation should be able to handle it. 
    * **Test_file.py** - This file will send a JSON request to the mentioned node.
    
3. **docker-compose.yml**: configuration to scale your image and create your cluster.
4. **Message.json**: Message structure which Raft Implementation will use for message passing between containers.  

## II Communication
We will be using sockets to communicate between different containers.

### III Message Structure
We will use JSON requests to communicate between the nodes. Messages contain the following fields -
* sender_name : node sending the message
* request : type of Message/Request
* term : current term of the sender
* key : message key
* value : message value

Different fields need to be populated for different messages.


### IV Type of Requests 
1. **Node Requests** - Sender name will be the name of the sender
* APPEND_RPC - Leader must send APPEND_RPC messages to let other nodes know of its presence 
* VOTE_REQUEST - Candidate should send VOTE_REQUEST messages to ask for votes from other nodes
* VOTE_ACK - VOTE_ACK must be sent back if the vote is granted to a requested vote, if not then drop/ignore.

2. **Controller Requests**
* CONVERT_FOLLOWER - convert the node to the follower state
* TIMEOUT - timeout the node immediately
* SHUTDOWN - shutdown all threads running on the node, no errors should be thrown
* LEADER_INFO - return leader info with key=LEADER and value=Node? which is the current leader

Sender name for node requests will be the node that sent the message, and "Controller" for all requests sent by the controller


### V Encoding/Decoding & UDP Packets
JSON requests are serialized and encoded to utf-8 before transmission. "Controller/convert_follower_node1.py" example 
shows how to do that in python. Post that the msg will be sent as UDP packets i.e. between nodes as well as the controller.

Similarly, at the receiving end we decode the JSON request on the receiving end before beginning our processing.


### VI IP and Ports
We use docker assigned IPs or container names on bridged networks in conjunction with 5555 as 
the port for all communication.

### VII Evaluation
Controller will be used to send different controller requests mentioned in section IV to interact with the system and test
out different configurations.

HOW TO USE THE TEST CASE?  
* Option1 - run convert_follower_node1.py from the DockerFile.
* Option2 - Open Controller CLI and run the following command to send a JSON Controller request
>python convert_follower_node1.py

Note : After starting, few seconds will be given for the system to stabilize and elect a leader before evaluation starts.

### Useful Links:
1) https://raft.github.io/
