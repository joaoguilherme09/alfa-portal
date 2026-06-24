# crypto.py — Alfa Profissionalizantes
# Por enquanto apenas bcrypt para senhas
# Criptografia dos dados sensíveis será implementada na Hostinger

import bcrypt

def hash_senha(senha):
    """Gera hash bcrypt da senha."""
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha, hash_armazenado):
    """Verifica se a senha bate com o hash."""
    return bcrypt.checkpw(senha.encode(), hash_armazenado.encode())

# Funções de criptografia — desativadas até migrar para Hostinger
def criptografar(valor):
    return valor

def descriptografar(valor):
    return valor