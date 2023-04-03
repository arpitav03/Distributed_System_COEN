# Distributed_System_COEN
To share Assignments

Description of the Assignment:

The goal of this programming assignment is to build a functional web server. The web server will be listening for the connections on a socket (bound to a specific port on the host machine).


Details:

For this programming assignment, I am implementing a HTTP web server program which can support multi-threading also. It accepts and responds to HTTP requests.
The Web server will be listening for connection on a socket and the clients will be connecting to this socket and will try to retrieve files from the server.
The client sends request to the server and when the connection is established, a timeout of 3 secs is used for keeping the connection alive for 3 secs. The default file is index.html, so if the user do not enter and filename, the default page will be loaded.
This web server responds with appropriate responses based on the requests provided to it. The different types of responses shown here are 200, 400, 403, 404, 500.
The server file is coded using python programming.
The port used is 8080.
