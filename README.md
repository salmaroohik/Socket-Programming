# Socket-Programming

Project:

Socket programming is a way of connecting two nodes on a network to communicate with each other. One socket(node) listens on a port at an IP, while another socket reaches out to the other to form a connection. Server forms the listener socket while the client reaches out to the server. The client needs to know of the existence of and the address of the server, but the server does not need to know the address of (or even the existence of) the client prior to the connection being established. Also, that once a connection is established, both sides can send and receive information. A socket is one end of an inter process communication channel. The two processes each establish their own socket. Our goal is to implement inter process communication between client and server using HTTP. We implemented this functionality by using Java as a coding language. We have deployed two scripts, each for the Client and the Server. We have used multi-threading in our script to handle multiple requests simultaneously.



Project-2:

Distance Vector Routing or DVR for short is a routing algorithm used to find the shortest/best route for data packets to traverse based on distance. There are a lot of factors involved in DVR such as cost, latency, and availability of routers but in this project, we will be focusing on cost. The term distance vector refers to the fact that the protocol manipulates vectors, arrays of distances to other nodes in the network. The distance vector algorithm was the original ARPANET routing algorithm and was implemented more widely in LANs with the Routing Information Protocol (RIP).
