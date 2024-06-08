from os import path
from re import search
from cryptography.fernet import Fernet
from Config import RELEASE_SYMMETRIC_KEY
from exceptions.IncorrectTemplate import IncorrectTemplateException

def read_file(f):
    if (path.exists(f) and path.isfile(f)):
        with open(f,"br") as op:
            return op.read()
    return b""

def determinator(size):
    if size < 1024:
        return (f'{size } B')
    elif size < 1024**2:
        return (f'{size // 1024 } kB')
    elif size < 1024**3:
        return (f'{size // 1024**2 } MB')
    elif size < 1024**4:
        return (f'{size // 1024**3 } GB')
    elif size < 1024**5:
        return (f'{size // 1024**4 } TB')
    
def template(text, variables):
    while (m := search(r"{{([^}]*)}}", text)) != None:
        var = m.group(1).strip()
        if var not in variables:
            raise IncorrectTemplateException("Incorrect variable", var)
        text = text.replace(m.group(0), str(variables[var]))
    return text

def encrypt_symmetric(data):
    return Fernet(RELEASE_SYMMETRIC_KEY).encrypt(data)

def decrypt_symmetric(data):
    return Fernet(RELEASE_SYMMETRIC_KEY).decrypt(data)