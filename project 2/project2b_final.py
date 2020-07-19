import socket
output_count=0
local_ip="127.0.0.1"# loaclhost or ip address of machine it self 
name="" #this will store node name
my_port="" #port number on which this node is listening
my_neighbour=[]  # list neighbour nodes
costs_found_in_file={}# this will have costs to neighbour, it will check while checking file for cost change
my_routing_table={} #Dictionary of shortest path to node, cost and next hop
file_name=input("give me file name to read=>") # to get file name
name=file_name[:file_name.index(".")] #seting node name by getting first character from file name
my_routing_table[name]={'cost':0,'hop':name} # adding distance to itself in routing table
'''
my_routing_table is nested dictonary
node will point to another dictinary conatning cost and hop
{'a':{'cost':2,'hop':'b'}}
'''
with open(file_name,"r") as f:
    '''
    opening file and reading lines for informations
    '''
    line1=f.readline()
    no_of_nodes,my_port=line1.split(" ")# reading first line, first word will be the count of neighbouring nodes and 2nd will be port no. this node will be using
    my_port=int(my_port)#converting string to int as file read will give string
    no_of_nodes=int(no_of_nodes)# doing same for no_of_nodes
    for i in range(no_of_nodes):
        line_for_node=f.readline()
        node,cost,port=line_for_node.split(" ") #here node is neighbour node, cost is cost to that neighbour,port is port on which that neighbour is listenging
        cost=float(cost)# coverting in float from string as asked in document
        costs_found_in_file[node]=cost# adding original cost to neighbour in costs_found_in_file for checking for update in file.
        my_neighbour.append(node+"->"+port) # adding a neighbour in my neigbour list and port on they listen with seprater "->"
        temp={'cost':cost,'hop':node}# temporary dictionary node will point to this dictionary
        my_routing_table[node]=temp # adding to routing tabel 
        
print("node | cost | Next hop")
'''
just printing routing table got from file 
'''
for s in my_routing_table:
    node=s
    temp=my_routing_table[s]
    cost=temp['cost']
    hop=temp['hop']
    print("%5s|%6s|%9s"%(node,cost,hop))

def readFromFileForUpdate():
    '''
    this function will read the file for update in cost of link,
    
    it will set the cost of neigbour node again i there is change

    it will also change the cost to other nodes if cost to hop(neighbour) is changed 
    '''
    global my_routing_table
    global costs_found_in_file
    with open(file_name,"r") as f:
        line1=f.readline()
        no_of_nodes,my_port=line1.split(" ")# reading first line first word will be count of neighbouring node and 2nd will be port no. this node will be using
        no_of_nodes=int(no_of_nodes)
        for i in range(no_of_nodes):
            line_for_node=f.readline()
            node,cost,port=line_for_node.split(" ") #here node is neighbour node, cost is cost to that neighbour,port is port on which that neighbour is listening
            cost=float(cost)
            if(cost==costs_found_in_file[node]):# checking for change in cost to neighbour if cost is same
                #if yes means no need of change
                continue
            else:
                #if no, change the cost to neighbour and other nodes where hop is node for which cost is change
                updateRoutingTable(cost,costs_found_in_file[node],node)
    
def updateRoutingTable(newCost,oldCost,hop):
    '''
    this function will update cost in routing table where ever hop is as "hop"
    
    it will do existing_cost=existing_cost-oldCost+newCost for updateing cost to other nodes

    node=>neighbouring node for which cost has change
    '''
    global my_routing_table
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ update in file detected")
    for i in my_routing_table:
        if(i==hop):#if hop and node is same, do update cost to neighbour in routing table
            my_routing_table[i]['hop']=hop
            my_routing_table[i]['cost']=newCost #setting new cost to my_routing_table
            costs_found_in_file[i]=newCost # updating the cost in costs_found_in_file as it will be change in file and will be require again for checking change in file
            continue
        if(my_routing_table[i]['hop']==hop):#if hop is same as node which has detected change, change cost to that node substract old_cost to that node and add new cost to that node
            my_routing_table[i]["cost"]+=newCost-oldCost

def printShortestPath():
    '''
    Its print routing table information in format asked by Prof.    
    '''
    global output_count # getting a global variable in function
    print("\nOutput Number >"+str(output_count))
    for i in my_routing_table:
        print("Shortest path "+name+"-"+i+": the next hop is "+my_routing_table[i]['hop']+" and the cost is "+str(my_routing_table[i]['cost']))
    output_count+=1

def sendRoutingTableToNeighbours():
    '''
    To send Routing table to adjacent nodes v2
    '''
    global name
    global my_neighbour
    global my_routing_table
    global Udp_socket
    for i in my_neighbour:
        str_to_send=name#initiating string_to_send to neighbour, starting with name of this node
        node_to_send,port_no_of_node_to_send=i.split("->") #neighbour will have data in format:-b->44444, getting name of neighbour and port on which it is listening
        port_no_of_node_to_send=int(port_no_of_node_to_send)
        '''
        ########## Implementing split horizon
        if hop is same as the neighbour program is sending routing table to, dont send that row
        '''
        for i in my_routing_table:
            if(my_routing_table[i]['hop']==node_to_send):#checking whether hop and neighbour are same
                # if yes don't add this row to string_to_send 
                continue
            hop=my_routing_table[i]['hop']
            cost=my_routing_table[i]['cost']
            str_to_send+=","+i+"'"+str(cost)+"'"+hop
        Udp_socket.sendto(str.encode(str_to_send),(local_ip,port_no_of_node_to_send))#this to send packet,
        #first argument is bytes to send (that why i used encode to conver string to bytes),
        #second arguments is ip addres and port no. (there are two arguments in second argument=>reciver ip and port)

def URTUM(msg):
    '''
    #Update Routing Table Using Message
    this will update routing table using message got from neighbours
    '''    
    global my_routing_table
    msg=msg.decode()# converting bytes to string
    tempList=msg.split(",")#temporary list, dividing message on bases of ","
    node_who_send=tempList[0]# name of node who sent this packet,    =>it is set in message while creating the, first part will be the name of node who send
    #assuming the packet sent by neigbhour so there will be entry in routing table
    cost_to_node_who_send=costs_found_in_file[node_who_send] # distance from current_node to node from which this packet came 
    got_routing_table=tempList[1:] # routing table we got from node, first term was name of the node who send and rest is routing table
    for i in got_routing_table: # for every entry in routing table with got in packet
        node,cost,hop=i.split("'")
        cost=float(cost)
        if node in my_routing_table: # if node is alreay in known node, we may need to update table
            if(my_routing_table[node]['hop']==node_who_send):#if for a row hop is same as the node from where this routing table arrived
                '''
                this will set distance of node which are acessible through node who send this table

                means if hop has found cost change ahead it will also change for current node
                '''
                my_routing_table[node]['cost']=cost+cost_to_node_who_send # set the cost sent by hop
            else:
                original_cost=my_routing_table[node]['cost'] #original cost to node in table
                new_cost=min(original_cost,(cost_to_node_who_send+cost))
                if (new_cost!=original_cost):# if we got new cost different from original_cost, we need to change the entry in routing table
                    my_routing_table[node]['cost']=new_cost# changing cost
                    my_routing_table[node]['hop']=node_who_send# changing hop
        else: #if node is not there in known node we need to add the node in known list
            my_routing_table[node]={"cost":cost+cost_to_node_who_send,"hop":node_who_send}
            



# output will start from here
import time
while(True):
    readFromFileForUpdate()# calling function to read update in file
    Udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # created a socket object with ipv4 configuration and to server udp protocol
    try:
        Udp_socket.bind((local_ip,my_port))
    except:
        print("another function is using same port:\n change the port")
        break
    Udp_socket.settimeout(5)# if after 5 second socket does not get any packet it will give timeoutException
    time.sleep(15)
    sendRoutingTableToNeighbours()# calling function to send current routing table to neighbours
    for i in range(len(my_neighbour)):# assuming only neigbour will send routing tables
        try:
            msg_from_neighbour,addr_of_neighbour=Udp_socket.recvfrom(1024)# if time out occurs there will exception
            URTUM(msg_from_neighbour)# it will call Update_Routing_Table_Using_Message with message got from packet 
        except:
            print("there suppose to be a packet, may be packet lost")
    printShortestPath()
input("press enter")
    
