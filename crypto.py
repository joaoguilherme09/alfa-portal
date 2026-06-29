import os
import bcrypt
from cryptography.fernet import Fernet

def get_fernet():
    chave = os.getenv('FERNET_KEY')
    if not chave:
        raise ValueError("FERNET_KEY não encontrada!")
    return Fernet(chave.encode())

def criptografar(valor):
    if not valor:
        return valor
    f = get_fernet()
    return f.encrypt(str(valor).encode()).decode()

def descriptografar(valor):
    if not valor:
        return valor
    try:
        f = get_fernet()
        return f.decrypt(str(valor).encode()).decode()
    except Exception:
        return valor  # retorna original se não conseguir descriptografar

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha, hash_armazenado):
    return bcrypt.checkpw(senha.encode(), hash_armazenado.encode())