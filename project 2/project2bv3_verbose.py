
'''
main difference between v1 and v2 is my_routing_tabel dataStructure is changed
to nested dictinary.

give video with documentation

there should be each node running before 10 seconds after running first node
otherwise there will exception, more more on this exception
https://stackoverflow.com/questions/44916411/pythons-udp-crashes-when-sending-to-ip-port-that-isnt-listening


version 3 has two more functions readFromFileForUpdate() and updateRoutingTable(newCost,oldCost,hop)
and also additional change in URTUM(msg) function
compare  hop and who_send_this packet
if equal means this is hop in table
set the provided cost
there may be change in cost ahead
'''

import socket
output_count=0
local_ip="127.0.0.1"# loaclhost or ip address of machine it self 
name="" #this node name
my_port="" #port number on which this node is listening
my_neighbour=[]  # list neighbour nodes
costs_found_in_file={}# this will have costs to neighbour, it will check while checking file for cost change
my_routing_table={} #list of shortest path to node, cost and next hop
file_name=input("give me file name to read=>") # to get file name
name=file_name[0] #seting node name by getting first character from file name
my_routing_table[name]={'cost':0,'hop':name} # adding distant to itself in routing table
# my_routing_table is nested dictonary

with open(file_name,"r") as f:
    line1=f.readline()
    no_of_nodes,my_port=line1.split(" ")# reading first line first word will be count of neighbouring node and 2nd will be port no. this node will be using
    my_port=int(my_port)
    no_of_nodes=int(no_of_nodes)
    for i in range(no_of_nodes):
        line_for_node=f.readline()
        node,cost,port=line_for_node.split(" ") #here node is neighbour node, cost is cost to that neighbour,port is port on which that neighbour is listenging
        cost=float(cost)
        costs_found_in_file[node]=cost# adding original cost to neighbour in costs_found_in_file.
        my_neighbour.append(node+"->"+port) # adding a know neighbou in my neigbour list and port on they listen
        temp={'cost':cost,'hop':node}# temporary dictionary
        my_routing_table[node]=temp # adding to routing tabel 
        
print("neighbour nodes=>"+str(my_neighbour))
#print("routing table=>"+str(my_routing_table))
##just for experiment not in need to add this in final code
print("node | cost | Next hop")
for s in my_routing_table:
    node=s
    temp=my_routing_table[s]
    cost=temp['cost']
    hop=temp['hop']
    print("%5s|%6s|%9s"%(node,cost,hop))

def readFromFileForUpdate():
    '''
    this function will read the file for update in cost of link
    it will set the cost of neigbour node again

    this will check if cost is changed tha it will update any thing 
    '''
    global my_routing_table
    global costs_found_in_file
    #local_routing_table=my_routing_table.copy() # to compare the new routing cost and existing one
    with open(file_name,"r") as f:
        line1=f.readline()
        no_of_nodes,my_port=line1.split(" ")# reading first line first word will be count of neighbouring node and 2nd will be port no. this node will be using
        no_of_nodes=int(no_of_nodes)
        for i in range(no_of_nodes):
            line_for_node=f.readline()
            node,cost,port=line_for_node.split(" ") #here node is neighbour node, cost is cost to that neighbour,port is port on which that neighbour is listenging
            print("after reading new line node=>,"+node+" cost=>,"+cost+" port=>"+port)
            cost=float(cost)
            if(cost==costs_found_in_file[node]):
                # checking for change in cost to neighbour
                print("###########################################################in if cost is not change")
                continue
            #my_routing_table[node]['cost']=cost
            else:
                #(cost!=my_routing_table[node]['cost']):
                print("before update costs_found_in_file=>"+str(costs_found_in_file))
                updateRoutingTable(cost,costs_found_in_file[node],node)
                print("after update costs_found_in_file=>"+str(costs_found_in_file))
    
def updateRoutingTable(newCost,oldCost,hop):
    '''
    this function will update cost in routing table where ever hop is as "hop"
    it will do existing_cost-oldCost+newCost
    '''
    global my_routing_table
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ update called")
    for i in my_routing_table:
        if(i==hop):#if hop is equal to node no change (change will be already made before calling this function)
            my_routing_table[i]['hop']=hop# it was required while changing the cost
            my_routing_table[i]['cost']=newCost #setting new cost to my_routing_table
            costs_found_in_file[i]=newCost # updating the cost as it is changed
            print("changing cost of "+i+" to =>"+str(newCost))
            continue
        if(my_routing_table[i]['hop']==hop):
            print("changing cost where hop=>"+hop+" from old cost=>"+str(my_routing_table[i]["cost"])+" to =>"+str(my_routing_table[i]["cost"]+newCost-oldCost))
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
    #print("\nstring to send=>"+str_to_send)
    for i in my_neighbour:
        str_to_send=name#string to send to neighbour
        node_to_send,port_no_of_node_to_send=i.split("->") #neighbour will have data in format:-b->44444
        print("sending routing table to node=>"+node_to_send)
        port_no_of_node_to_send=int(port_no_of_node_to_send)
    #creating local routing table or implementing split horizon
        for i in my_routing_table:
            if(my_routing_table[i]['hop']==node_to_send):
                continue
            hop=my_routing_table[i]['hop']
            cost=my_routing_table[i]['cost']
            str_to_send+=","+i+"'"+str(cost)+"'"+hop
        Udp_socket.sendto(str.encode(str_to_send),(local_ip,port_no_of_node_to_send))#this to send packet, first argument is bytes to send (that why is used encode to conver string to bytes),
        #second arguments is ip addres and port no. (there are two arguments in secondr argument=>reciver ip and port)
        print("packet sent with string =>"+str_to_send)
    #Udp_socket.sendto(str.encode(str_to_send),(local_ip,))

def URTUM(msg): #Update Routing Table Using Message
    global my_routing_table
    msg=msg.decode()
    tempList=msg.split(",")#temporary list
    node_who_send=tempList[0]# name of node who sent this packet
    print("\nthis packet was sent by=>"+node_who_send)
    #assuming the packet sent by neigbhour so there will be entry in routing table
    cost_to_node_who_send=costs_found_in_file[node_who_send] # distance from current_node to node from which this packet came 
    got_routing_table=tempList[1:] # routing table we got from node, first term was name of node who send and rest is table
    print("got routing table"+str(got_routing_table))
    for i in got_routing_table: # for every entry in routing table with got in packet
        node,cost,hop=i.split("'")
        cost=float(cost)
        if node in my_routing_table: # if node is alreay in known node list we may need to update table
            if(my_routing_table[node]['hop']==node_who_send):#if for a row hop is same as the node from where this routing table arries
                '''
                this will set distance of node which are acessible
                from the hop when hop send the routing table 
                '''
                my_routing_table[node]['cost']=cost+cost_to_node_who_send # set the cost sent by hop
            else:
                original_cost=my_routing_table[node]['cost'] #original cost to node in table
                print("minimum from, original cost=>"+str(original_cost)+"and cost_to_node_who_send+cost=>"+str(cost_to_node_who_send+cost))
                new_cost=min(original_cost,(cost_to_node_who_send+cost))
                if (new_cost!=original_cost):# if we got new cost different original cost, we need to change the entry in routing table
                    my_routing_table[node]['cost']=new_cost
                    my_routing_table[node]['hop']=node_who_send
        else: #if node is not there in known node we need to add the node in known list
            my_routing_table[node]={"cost":cost+cost_to_node_who_send,"hop":node_who_send}
            



# output will start from here
import time
while(True):
    printShortestPath()
    readFromFileForUpdate()
    Udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # created a socket object with ipv4 configuration and to server udp protocol
    Udp_socket.bind((local_ip,my_port))
    Udp_socket.settimeout(5)# if after 5 second socket does not get any packet it will give timeoutException
    time.sleep(15)
    sendRoutingTableToNeighbours()
    print("listening on port "+str(my_port)+" for udp packet from neighbour")
    for i in range(len(my_neighbour)):# assuming only neigbour will send routing tables
        try:
            msg_from_neighbour,addr_of_neighbour=Udp_socket.recvfrom(1024)
            URTUM(msg_from_neighbour)
        except:
            print("there suppose to be a packet, may be packet lost")        
#input("getch()")
