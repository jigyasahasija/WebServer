import socket
import threading
import time

def thread_func(conn,address):
    file_path = "www"
    dataRecieved = conn.recv(2048).decode()  ##receives http request data from the socket
    request = dataRecieved.split("\r\n")
    requestStr = "" + request[0]
    requestStr = requestStr.split(' ')
    path = requestStr[1]
    if(path.__eq__("/") or path.__eq__("/index.html")):
        if(not path.__eq__("/")):
            file = open(file_path+f"/{path}","r")
        else:
            file = open(file_path+"/index.html","r")
        response =  f"HTTP/1.1 200 OK\r\n\r\n{file.read()}\r\n"
        
    else:
        response = f"HTTP/1.1 404 Not Found\r\n\r\nNot a valid path: {path}\r\n"

    response = bytes(response, 'utf-8')

    print(f"Thread for client {address}")
    time.sleep(5)
    conn.send(response)
    conn.close()
    print(f"Connection closed with {address}")

HOST = "127.0.0.1"    ##IP address of our server
PORT= 1025            ##Port number of our server 
threads = []

socket_obj = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)  ##socket instance
socket_obj.bind((HOST,PORT))
socket_obj.settimeout(30)

print(f"Listening enabled on {HOST},{PORT}")

try:
    while True:
        socket_obj.listen(1)
        print("Waiting for a client")
        conn, address = socket_obj.accept()
        print(f"Connected with {address}")
        conn.settimeout(1)
        th = threading.Thread(target=thread_func,args=(conn,address,))
        threads.append(th)
        th.start()
        print("Out of thread")
except socket.timeout as e:
    print ("Timeout is over")
    print (e)
finally:
    if socket_obj:
        socket_obj.close()
    for t in threads:
        t.join()
        print(f"Thread closing for client {address}")