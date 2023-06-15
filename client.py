import socket
from encoding import useKey
from time import sleep
import customtkinter as ctk
from os.path import basename
#параметры
host = '192.168.1.17'
port = 1234
buff_size = 1024
private_key, public_key = None, None



def sendFile(client, file_name):
    #client.send(command.encode())
    #print(file_name)
    try:
        file = open(file_name, 'rb')
    except:
        print(f"[CLIENT] Can't open sended file: {file_name}")
    data = file.read(buff_size)
    while data:
        client.send((data))
        data = file.read(buff_size)

    client.send(b'<END>')  
    print('[CLIENT] msg shared!')  
    
def recieveFile(client, file_name):
    
    file = open(file_name, 'wb')
    data = client.recv(buff_size)
    while data[-5:] != b'<END>':
        file.write(data)
        data = client.recv(buff_size)
    
    if(len(data) > 5):
        file.write(data[0:-5])
        

    print("[CLIENT]  transfered succesfully")
    
    file.close()
      

def ServerMeet(socket_, command : str):
    #command = input()
    
    #while command != 'exit':
    
    cmd_ = command[0:command.find(' ')]
    if cmd_ == 'send_file':
       # filepath = ctk.filedialog.askopenfilename()
       # print(filepath)
        socket_.send( (cmd_+ ' ' + basename(command[command.find(' ')+1:])).encode() )
        file_name = command[command.find(' ')+1:]
        sendFile(socket_, file_name)
    elif cmd_ == 'use_key':
        socket_.send(command.encode())
        with open(command[command.find(' ')+1:], 'rb') as f:
            data = f.read(1024)
        socket_.send(data)
        #private_key = useKey(command[command.find(' ')+1:])
        #socket_.send(private_key.encode())
    elif cmd_ == 'use_key_pub':
        socket_.send(command.encode())
        with open(command[command.find(' ')+1:], 'rb') as f:
            data = f.read(1024)
        socket_.send(data)
    elif cmd_ == 'encode_file':
        socket_.send(command.encode())  
        recieveFile(socket_, command[command.find(' ')+1:]+'.sig')
        #recieveFile(socket_, '3.png.sig')
    elif cmd_ == 'verify_sign':
        socket_.send(command.encode())
        return socket_.recv(buff_size).decode()
    elif cmd_ == 'send_encode_file': #send_encode_file <path>
        socket_.send(command.encode())
        file_name = command[command.find(' ')+1:]
        sendFile(socket_, file_name)
        recieveFile(socket_, command[command.find(' ')+1:]+'.sig')
    elif cmd_ == 'rec_file':
        socket_.send(command.encode())
        file_name = command[command.find(' ')+1:]
        recieveFile(socket_, file_name)
        #command = input()
    elif cmd_ == 'upload_file':
        socket_.send((cmd_+ ' ' + basename(command[command.find(' ')+1:])).encode())
        file_name = command[command.find(' ')+1:]
        sendFile(socket_, file_name)
        
        
    elif command == 'exit':
        socket_.send(command)
        socket_.close()
    return None
    #socket_.close()
#socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket_.connect((host, port))

#ServerMeet(socket_, '')