from ecdsa import SigningKey, NIST256p, VerifyingKey
from ecdsa import BadSignatureError
from ecdsa.util import sigdecode_der, sigencode_der
from zlib import crc32 
from hashlib import sha256

def useKey(path):
    try:
        with open(path, 'rb') as f:
            return SigningKey.from_pem(f.read())
    except:
        print(f"Failed can't use key in {path}")
        return None
    
def UsePub(path):
    try:
        with open(path, 'rb') as f:
            return VerifyingKey.from_pem(f.read())
    except:
        print(f"Failed can't use key in {path}")
        return None
    

def EncodeFile(path, private_key):
    if private_key == None:
        print("Can't make sig, choose private_key")
        return None

    #чтение файла
    try:
        with open(path, 'rb') as file:    
            data = sha256(file.read()).hexdigest().encode()
            #   data = b'\n\x00\x00\x00\x00'
    except:
        print(f'[SERVER] Cant open file {path}')
    try:

        sig = private_key.sign_deterministic(data, sigencode=sigencode_der, hashfunc=sha256)
        #запись подписи в файл
        with open(path+'.sig', 'wb') as siq_file:
            siq_file.write(sig)
        print(f'[CLIENT] File: {path} signigied')
    except:
        print("Can't make sig")

def VerifyFile(path_sig, path_source, public_key):
    if public_key == None:
        print("Can't verify sig without public_key")
        return None
    try:
        with open(path_sig, 'rb') as f:
            sig = f.read()
    except:
        print("Can't open sig file")
    try:    
        with open(path_source, 'rb') as file:    
            data = sha256(file.read()).hexdigest().encode()
    except:
        print("Can't open source file")
    try:
        res = public_key.verify(sig, data, hashfunc=sha256, sigdecode=sigdecode_der)
        return res
        assert res
        print('[CLIENT] Valid sign')
    except BadSignatureError:
        print('[CLIENT] Invalid sign')

