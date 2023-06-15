import tkinter as tk
import customtkinter as ctk
from PIL import Image
from encoding import useKey, EncodeFile, VerifyFile, UsePub
from os import getcwd
from os.path import basename
import socket
from client import sendFile, recieveFile, ServerMeet

#параметры
host = '192.168.1.17'
port = 1234
buff_size = 1024

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.cur_dir = getcwd()

        self.resizable(1,1)
        
        self.private_key = None
        self.public_key = None

        self.encode_file_path = None
        
        self.verify_file_path = None
        self.source_file =  None

#socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket_.connect((host, port))

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
        except:
            print(f"Can't connect to: {host, port}")
            
       # recieveFile(self.client, 'ar.png')

        self.client.send('login ilya'.encode())
        self.geometry('800x600')

        #set grid 1 row, 2 columns
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        #self.grid_columnconfigure(2, weight=1)
        self.columnconfigure(0, minsize=230)
        self.columnconfigure(1, weight=1, minsize=700)
        #self.rowconfigure(0, minsize=600)
        
        #load images
        logo_image = ctk.CTkImage(Image.open('images\\armadillo (1).png'), size = (60, 60)) 
        add_image = ctk.CTkImage(Image.open('images\\cloud.png'), size = (30, 30))
        #folder_image = ctk.CTkImage(Image.open('folder.png'), size = (30, 30))
        encode_image = ctk.CTkImage(Image.open('images\\key.png'), size = (30, 30))
        verify_image = ctk.CTkImage(Image.open('images\\verify.png'), size = (30, 30))
        self.lablekey_image = ctk.CTkImage(Image.open('images\\key2.png'), size = (400, 400))
        self.lablecloud_image = ctk.CTkImage(Image.open('images\\cloud.png'), size = (400, 400))
        self.lableverify_image1 = ctk.CTkImage(Image.open('images\\cross.png'), size = (400, 400))
        self.lableverify_image2 = ctk.CTkImage(Image.open('images\\verify.png'), size = (400, 400))
        self.table_image = ctk.CTkImage(Image.open('images\\table.png'), size = (512, 512))
        #frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, width=400)
        self.navigation_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
       # self.navigation_frame.grid_rowconfigure(2, weight=1)
       
        #lable
        self.lable_logo = ctk.CTkLabel(self.navigation_frame, corner_radius=0, image=logo_image, font=ctk.CTkFont(size=20, weight="bold"), compound='left', text='signify      ')
        self.lable_logo.grid(row=0, column = 0, padx = 20, pady = 15)
        
        
        #buttons        
        self.add_button = ctk.CTkButton(self.navigation_frame, text=' upload file', image=add_image, compound='left', height=40, fg_color='#C57A44', command=self.upload_cloud)
        self.add_button.grid(row=1, column = 0, sticky = 'nsew', padx=10, pady=5)

        self.verify = ctk.CTkButton(self.navigation_frame, text=' verify sign', image=verify_image, compound='left', height=40, fg_color='#C57A44', command=self.verify_main)
        self.verify.grid(row=2, column = 0, sticky = 'ew', padx=10, pady=5)

        self.encode = ctk.CTkButton(self.navigation_frame, text=' make sign', image=encode_image, compound='left', height=40, command=self.encode_main, fg_color='#C57A44')
        self.encode.grid(row=3, column = 0, sticky = 'ew',padx=10, pady=5)
        
        #main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
      #  self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid(row=0, column=1, padx=10, pady = 10, sticky = 'nsew')
        
        self.label = ctk.CTkLabel(self.main_frame, corner_radius=0, image=self.table_image, font=ctk.CTkFont(size=20, weight="bold"), compound='left', text='')
        self.label.grid(row=0,column=1, padx=25, pady = 25)

        
        #buttons for verify page
       # self.button_verify = ctk.CTkButton(self.main_frame, )
    def __del__(self):
        self.client.send('exit'.encode())
        self.client.close()

    def encode_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


        #Label 
        self.label = ctk.CTkLabel(self.main_frame, corner_radius=0, text='Выберите файл и ключ для шифрования:', 
                                  image=self.lablekey_image, compound='top', anchor=ctk.CENTER,font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=2)
        
        
        #buttons for encode page
        self.button_file = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Private key', fg_color='#C57A44', 
                                         command=lambda: self.pick_file(('Pem Files', '*.pem'), 'private_key'))
        self.privateKey_file = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Signing file', fg_color='#C57A44', 
                                             command=lambda: self.pick_file(('All files', '*.*'), 'encode_file_path'))
        
        #self.sign_file = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Make sign', fg_color='#C57A44', command=lambda : EncodeFile(self.encode_file_path, self.private_key))
        self.sign_file = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Make sign', fg_color='#C57A44', 
                                       command=lambda : ServerMeet(self.client, f'encode_file {basename(self.encode_file_path)}'))
        
        
        self.button_file.grid(row=1, column = 2, sticky = 'nsew', padx=10, pady=5)
        self.privateKey_file.grid(row=2, column = 2, sticky = 'ew', padx=10, pady=5)
        self.sign_file.grid(row=3, column=2, sticky = 'ew', padx=10, pady=5)


   # def pick_and_send(self, name):
    #    if (name == "private_key"):

    def verify_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        self.label = ctk.CTkLabel(self.main_frame, corner_radius=0, text='Выберите подписанный файл, исходный файл и открытый ключ:', 
                                  image=self.lablekey_image, compound='top', anchor=ctk.CENTER,font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.main_frame.rowconfigure(3, weight=1)
        
        self.label.columnconfigure(1, weight=1)
        
        
        self.publicKey_file = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Public key', fg_color='#C57A44', 
                                            command=lambda: self.pick_file(('Pem Files', '*.pem'), 'public_key'))
        self.signed_file = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Signed file', fg_color='#C57A44', 
                                         command=lambda: self.pick_file(('All files', '*.*'), 'signed_file'))
        self.source_file = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Source file', fg_color='#C57A44', 
                                         command=lambda: self.pick_file(('All files', '*.*'), 'source_file'))
        self.verify_file = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Check sign', fg_color='#C57A44', 
                                         command=lambda : 
                            self.VerifyFile_(path_sig = self.verify_file_path, path_source=self.source_file))
        
        
        self.publicKey_file.grid(row=1, column = 1, sticky = 'ew', padx=10, pady=5)
        self.signed_file.grid(row=2, column = 1, sticky = 'ew', padx=10, pady=5)
        self.source_file.grid(row=3, column = 1, sticky = 'ew', padx=10, pady=5)
        self.verify_file.grid(row=4, column=1, sticky = 'ew', padx=10, pady=5)

        
    def VerifyFile_(self, path_sig, path_source):
        res = ServerMeet(self.client, f"verify_sign {basename(path_sig)} {basename(path_source)}")
        #print(res, res == True)
        if res == 'True':
            self.label.configure(image = self.lableverify_image2)
        else:
            self.label.configure(image = self.lableverify_image1)
       # else:
        #    self.label.configure(image = self.lableverify_image1)
            
            
    def upload_cloud(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        self.label = ctk.CTkLabel(self.main_frame, corner_radius=0, text='Выберите файл, чтобы загрузить его в облако:', 
                                  image=self.lablecloud_image, compound='top', anchor=ctk.CENTER,font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=1)
        self.label.grid_rowconfigure(0, weight=1)
        self.label.grid_columnconfigure(1, weight=1)
        self.source_file2 = ctk.CTkButton(self.main_frame, corner_radius=0, text = 'Source file', fg_color='#C57A44', 
                                         command=lambda: self.pick_file(('All files', '*.*'), 'upload_file'))
        self.source_file2.grid(row=1, column=1)
        
    
         
    def pick_file(self, format, name):
        filepath = ctk.filedialog.askopenfilename(filetypes=[format])
        if filepath != '':
            if name == 'private_key':
                self.private_key = useKey(filepath)
                #self.client.send('use_key ')
                ServerMeet(self.client, f'use_key {(filepath)}')
                #self.public_key = self.private_key.verifying_key
                if self.private_key != None:
                    print('Readed key')
            elif name == 'public_key':
                self.public_key = UsePub(filepath)
                ServerMeet(self.client, f'use_key_pub {(filepath)}')

            elif name == 'encode_file_path':
                self.encode_file_path = filepath
                ServerMeet(self.client, f'send_file {filepath}')
                #self.SendFile_()

            elif name == 'signed_file':
                self.verify_file_path = filepath
                ServerMeet(self.client, f'send_file {filepath}')

            elif name == 'source_file':
                self.source_file = filepath
                ServerMeet(self.client, f'send_file {filepath}')
            elif name == 'upload_file':
                self.source_file = filepath
                ServerMeet(self.client, f'upload_file {filepath}')
        

        print(filepath)



    
    def p(self):
        print("WTF??")

''' 
    TODO:   загрузить на серв бд логин пароль
            иметь возможность скачаить из папки
            удаляить на серве файл после откачки на облако
            покрасивее графику
            

'''
        
if __name__ == '__main__':
    app = App()
    app.mainloop()