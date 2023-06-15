import socket 
import threading
from encoding import EncodeFile, VerifyFile
from ecdsa import SigningKey
#параметры
host = '192.168.1.32'#
port = 1234
buff_size = 1024
private_key, public_key = None, None

def recieveFile(client, file_name):
    file = open(file_name, 'wb')
    data = client.recv(buff_size)
    while data[-5:] != b'<END>':
        file.write(data)
        data = client.recv(buff_size)
    
    if(len(data) > 5):
        file.write(data[0:-5])
        

    print("[SERVER]  transfered succesfully")
    
    file.close()
    
def sendFile(socket_, file_name):
    socket_.send(file_name.encode())
    print(file_name)
    file = open(file_name, 'rb')
    data = file.read(buff_size)
    while data:
        socket_.send((data))
        data = file.read(buff_size)
    socket_.send(b'<END>')  
    print('[CLIENT] msg shared!')

def recieveData(client):
    while True:
        try:
            command = client.recv(buff_size).decode()
            print(f'[SERVER] Recieved command: {command}')
            s = command.split(' ')
            print(command)
            if s[0] == 'send_file': # file: client -> server
                recieveFile(client, s[1])
            elif s[0] == 'use_key': #use_file <path>
                f = client.recv(buff_size)
                private_key = SigningKey.from_pem(f)
                verify_key = private_key.verifying_key
                if private_key == None:
                    print('failed key reading')
                #private_key = useKey(s[1])
                #verify_key = private_key.verifying_key
            elif s[0] == 'encode_file':#encode_file <path>
                EncodeFile(s[1], private_key)
                sendFile(client, s[1]+'.sig')
            elif s[0] == 'verify_sign':#verify_sign <source file> <signed file>
                print(VerifyFile(s[1], s[2], verify_key))
            elif s[0] == 'send_encode_file':
                #recieveFile(client, s[1])
                EncodeFile(s[1], private_key)
                #sendFile()

            elif s[0] == 'send_encode_file_with_key':
                #file_name = 
                recieveFile(client, s[1])
                f = client.recv(buff_size)
                private_key = SigningKey.from_pem(f)
                verify_key = private_key.verifying_key
                print('Here')
                EncodeFile(s[1], private_key)
                client.send((s[1]+".sig").encode())
                sendFile(client, s[1]+'.sig')
                print(f'[SERVER] file {s[1]} signed and sended back')

            elif s[0] == 'rec_file':
                sendFile(client, s[1])



            elif s[0] == 'exit':
                print(f'[SERVER] client disconnected')
                client.close()
                break    
            else:
                print('[SERVER] Unknown command')
        except:
            pass
        #else:
            #print(f'[SERVER] Unknown command: {command}')
        #print(command)
        #recieveFile(client, command)
        
            

            


socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_.bind((host, port))
socket_.listen(16)
print(f"[Server listening...]")

def recieve():
    while True:
        try:
            conn, addr = socket_.accept()
        #регает новые подключения
            print(f"[New connection]: {addr}")
        
            thread = threading.Thread(target=recieveData, args=(conn,))
            thread.start()
        except:
            print("Can't connect")
        '''
        file_name = conn.recv(buff_size).decode()
        print(file_name)

        file = open(file_name, 'wb')

        data = conn.recv(buff_size)
        while data:
            file.write(data)
            data = conn.recv(buff_size)

        print("[SERVER]  transfered succesfully")
        '''
        
    


    conn.close()
    #conn, addr = socket_.accept()
#регает новые подключения
#print(f"[New connection]: {conn}, from: {addr}")
#m = conn.recv(buff_size).decode()
#print(m)




recieve()
socket_.close()