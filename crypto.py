# crypto.py — Alfa Profissionalizantes
# Funções de criptografia para dados sensíveis

import os
import bcrypt
from cryptography.fernet import Fernet

# ===== CHAVE FERNET =====
# Gera uma chave e salva no .env na primeira vez
# Nunca mude essa chave depois que tiver dados no banco!

def get_fernet():
    chave = os.getenv('FERNET_KEY')
    if not chave:
        raise ValueError("FERNET_KEY não encontrada no .env!")
    return Fernet(chave.encode())

# ===== FERNET — criptografia reversível =====

def criptografar(valor):
    """Criptografa um valor. Retorna string."""
    if not valor:
        return valor
    f = get_fernet()
    return f.encrypt(str(valor).encode()).decode()

def descriptografar(valor):
    """Descriptografa um valor. Retorna string."""
    if not valor:
        return valor
    try:
        f = get_fernet()
        return f.decrypt(str(valor).encode()).decode()
    except Exception:
        return valor  # Se falhar, retorna o valor original (dados antigos não criptografados)

# ===== BCRYPT — hash irreversível (senhas) =====

def hash_senha(senha):
    """Gera hash bcrypt da senha."""
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha, hash_armazenado):
    """Verifica se a senha bate com o hash."""
    return bcrypt.checkpw(senha.encode(), hash_armazenado.encode())