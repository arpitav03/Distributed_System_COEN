# Programming Assignment 1 : Distributed Systems (COEN 317) - Winter 2023
# Name: Arpita Verma
# SCU ID : W1632653

# Objective: To build a functional web server using the following high level structure

# Forever loop: 
    # Listen for connections
    # Accept new connection from incoming client
    # Parse HTTP request
    # Ensure well-formed request (return error otherwise)
    # Determine if target file exists and if permissions are set properly (return error otherwise)
    # Transmit contents of file to connect (by performing reads on the file and writes on the socket)
    # Close the connection

import socket
import os
import threading
import sys
import argparse
import time
import signal

HOST = "localhost"
PORT = 8080 # Defining the default port to be used
DIR = './'  # Default Directory


def Live_connection(conn, addr):
    size = 1024
    with conn:
        conn.setTimeout(3)
        while True:
            try:
                Socket_Req = conn.recv(size).decode()   
                Socket_Head = Socket_Req.split('\r\n')   
                RESULT  = Socket_Head[0].split()
                if RESULT[0] == "GET":
                    HTTP_Conn_Thread(RESULT,conn) # function defined below
            except Exception as EXP:
                break
    conn.close() #closing the connection


def HTTP_Conn_Thread(Socket_Req, conn):
    print(Socket_Req)
    if(Socket_Req[1] == '/'):
        Socket_Req[1] = '/index.html'
    try:
        if(Socket_Req[1].find('.html') > 0 or Socket_Req[1].find('.txt') > 0):
            FLNM = DIR + Socket_Req[1]
            with open(FLNM,  'r', encoding='latin-1') as FILE:
                content = FILE.read()
            FILE.close()
            Socket_Response = str.encode("HTTP/1.1 200 OK\n") # Response Code 200
            Socket_Response = Socket_Response + str.encode('Content-Type: text/html\n')
            Socket_Response = Socket_Response + str.encode('\r\n')
            conn.sendall(Socket_Response)
            conn.sendall(content.encode())
        
        elif(Socket_Req[1].find('.mp4') > 0):   
            conn.sendall(str.encode("HTTP/1.1 403 Forbidden\r\nForbidden")) # Response Code 403
        
        elif(Socket_Req[1].find('.png') > 0 or Socket_Req[1].find('.jpg') > 0 or Socket_Req[1].find('.gif') > 0): #Checking the different image types
            IMG_EXTN = Socket_Req[1].split('.')[1]  #Image Extension
            FLNM = '.' + Socket_Req[1]
            image_data = open(FLNM, 'rb')
            Socket_Response = str.encode("HTTP/1.1 200 OK\n") # Response Code 200
            IMG_EXTN = "Content-Type: image/" + IMG_EXTN +"\r\n"
            Socket_Response = Socket_Response + str.encode(IMG_EXTN)
            Socket_Response = Socket_Response + str.encode("Accept-Ranges: bytes\r\n\r\n")
            conn.sendall(Socket_Response)
            conn.sendall(image_data.read())
			
        elif(Socket_Req[1].find('*') > 0 or Socket_Req[1].find('!') > 0):   
            conn.sendall(str.encode("HTTP/1.1 400 Bad Request\r\nBad Request")) # Response Code 400
			
        else:
            conn.sendall(str.encode("HTTP/1.1 404 NOT FOUND\r\nFile Not Found")) # Response code 404
    except FileNotFoundError: 
       conn.sendall(str.encode("HTTP/1.1 404 NOT FOUND\r\nFile Not Found")) # Response code 404
	   
    except Exception:
       conn.sendall(str.encode("HTTP/1.1 500 Internal Server Error\r\nInternal Server Error"))  #Response Code 500
    
	
def Socket_listen():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Socket_List:
        Socket_List.bind((HOST, PORT))  # Socket binded to the port
        while True:
            Socket_List.listen() 
            conn, addr = Socket_List.accept() # Accepting new connection from incoming client
            MULTITHREAD = threading.Thread(target=Live_connection, args=(conn, addr)) # Live_connection fn defined above with arguments as connection and address of the socket
            MULTITHREAD.start()

# Main Function to run the code	
if __name__ == "__main__":

    inputArgs = argparse.ArgumentParser()
    inputArgs.add_argument('-document_root', type=str)
    inputArgs.add_argument('-port', type=int)
    parsedArgs = inputArgs.parse_args()
    try:
        PORT = parsedArgs.port
        DIR = parsedArgs.document_root
    except AttributeError:
        print("Arguments are missing or input type is wrong")
        print("Input type = python server.py -document_root './' -port 8080")
        sys.exit(1)
    print("Server host and port" + HOST + ":" + str(PORT))
    print("Server directory:" + DIR)
    Socket_listen()  # Function defined above
