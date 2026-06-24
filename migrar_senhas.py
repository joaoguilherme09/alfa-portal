# migrar_senhas.py
# Roda UMA VEZ para migrar senhas em texto puro para bcrypt
# Execute: python migrar_senhas.py

import bcrypt
from db import create_connection, get_cursor

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

conn = create_connection()
cur  = get_cursor(conn)

# Buscar todos os professores
cur.execute("SELECT id, matricula, senha FROM portal_professores")
professores = cur.fetchall()

for p in professores:
    senha_atual = p['senha']
    # Só migra se não for um hash bcrypt (hashes bcrypt começam com $2b$)
    if not senha_atual.startswith('$2b$'):
        novo_hash = hash_senha(senha_atual)
        cur.execute("UPDATE portal_professores SET senha = %s WHERE id = %s", (novo_hash, p['id']))
        print(f"Professor {p['matricula']}: senha migrada")
    else:
        print(f"Professor {p['matricula']}: já está em bcrypt")

# Buscar todos os alunos
cur.execute("SELECT id, matricula, senha FROM portal_alunos")
alunos = cur.fetchall()

for a in alunos:
    senha_atual = a['senha']
    if not senha_atual.startswith('$2b$'):
        novo_hash = hash_senha(senha_atual)
        cur.execute("UPDATE portal_alunos SET senha = %s WHERE id = %s", (novo_hash, a['id']))
        print(f"Aluno {a['matricula']}: senha migrada")
    else:
        print(f"Aluno {a['matricula']}: já está em bcrypt")

conn.commit()
cur.close()
conn.close()
print("\nMigração concluída!")