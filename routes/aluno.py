from flask import Blueprint, render_template, session, redirect, url_for
from db import create_connection, get_cursor

aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')

NOMES_MESES = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorador(*args, **kwargs):
        if session.get('perfil') != 'aluno':
            return redirect(url_for('auth.login_aluno'))
        return f(*args, **kwargs)
    return decorador

@aluno_bp.route('/home')
@login_required
def home():
    return render_template('aluno/home.html')

@aluno_bp.route('/notas')
@login_required
def notas():
    aluno_id = session['id']

    conn = create_connection()
    cur  = get_cursor(conn)

    cur.execute("""
        SELECT mes, COUNT(*) as qtd
        FROM portal_notas
        WHERE aluno_id = %s AND ano = YEAR(NOW())
        GROUP BY mes
    """, (aluno_id,))
    notas_por_mes_raw = cur.fetchall()

    cur.execute("""
        SELECT nome_atividade, mes, ano, valor,
               DATE_FORMAT(criado_em, '%d/%m/%Y') as data
        FROM portal_notas
        WHERE aluno_id = %s
        ORDER BY criado_em DESC
        LIMIT 10
    """, (aluno_id,))
    ultimas = cur.fetchall()
    cur.close()
    conn.close()

    notas_por_mes = {n['mes']: n['qtd'] for n in notas_por_mes_raw}

    return render_template('aluno/notas.html',
        notas_por_mes=notas_por_mes,
        ultimas=ultimas,
        nomes_meses=NOMES_MESES
    )

@aluno_bp.route('/notas/<int:mes>')
@login_required
def notas_mes(mes):
    aluno_id = session['id']
    nome_mes = NOMES_MESES.get(mes, 'Mês')

    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        SELECT nome_atividade as nome, valor,
               DATE_FORMAT(criado_em, '%d/%m/%Y') as data
        FROM portal_notas
        WHERE aluno_id = %s AND mes = %s AND ano = YEAR(NOW())
        ORDER BY criado_em DESC
    """, (aluno_id, mes))
    notas = cur.fetchall()
    cur.close()
    conn.close()

    media = round(sum(n['valor'] for n in notas) / len(notas), 2) if notas else 0

    return render_template('aluno/notas_mes.html',
        nome_mes=nome_mes, notas=notas, media=media)

@aluno_bp.route('/faltas')
@login_required
def faltas():
    aluno_id = session['id']

    conn = create_connection()
    cur  = get_cursor(conn)

    cur.execute("""
        SELECT MONTH(data_aula) as mes, COUNT(*) as qtd
        FROM portal_chamadas
        WHERE aluno_id = %s AND status = 'F' AND YEAR(data_aula) = YEAR(NOW())
        GROUP BY MONTH(data_aula)
    """, (aluno_id,))
    faltas_por_mes_raw = cur.fetchall()

    cur.execute("""
        SELECT MONTH(data_aula) as mes,
               DATE_FORMAT(data_aula, '%d/%m/%Y') as data,
               t.nome as turma
        FROM portal_chamadas c
        JOIN portal_turmas t ON t.id = c.turma_id
        WHERE c.aluno_id = %s AND c.status = 'F' AND YEAR(data_aula) = YEAR(NOW())
        ORDER BY data_aula
    """, (aluno_id,))
    faltas_detalhe_raw = cur.fetchall()
    cur.close()
    conn.close()

    faltas_por_mes = {f['mes']: f['qtd'] for f in faltas_por_mes_raw}

    faltas_detalhe = {}
    for f in faltas_detalhe_raw:
        m = f['mes']
        if m not in faltas_detalhe:
            faltas_detalhe[m] = []
        faltas_detalhe[m].append({'data': f['data'], 'materia': f['turma']})

    return render_template('aluno/faltas.html',
        faltas_por_mes=faltas_por_mes,
        faltas_detalhe=faltas_detalhe,
        nomes_meses=NOMES_MESES
    )

@aluno_bp.route('/comentarios')
@login_required
def comentarios():
    aluno_id = session['id']

    conn = create_connection()
    cur  = get_cursor(conn)

    # Buscar turmas do aluno
    cur.execute("""
        SELECT turma_id FROM portal_aluno_turma WHERE aluno_id = %s
    """, (aluno_id,))
    turmas = [t['turma_id'] for t in cur.fetchall()]

    if turmas:
        formato = ','.join(['%s'] * len(turmas))
        cur.execute(f"""
            SELECT titulo, arquivo, DATE_FORMAT(criado_em, '%d/%m/%Y') as data
            FROM portal_comunicados
            WHERE (tipo = 'turma' AND turma_id IN ({formato}))
               OR (tipo = 'aluno' AND aluno_id = %s)
            ORDER BY criado_em DESC
        """, (*turmas, aluno_id))
    else:
        cur.execute("""
            SELECT titulo, arquivo, DATE_FORMAT(criado_em, '%d/%m/%Y') as data
            FROM portal_comunicados
            WHERE tipo = 'aluno' AND aluno_id = %s
            ORDER BY criado_em DESC
        """, (aluno_id,))

    comunicados = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('aluno/comentarios.html', comunicados=comunicados)


@aluno_bp.route('/notificacoes')
@login_required
def notificacoes():
    aluno_id = session['id']
    conn = create_connection()
    cur  = get_cursor(conn)

    # Notas dos últimos 7 dias
    cur.execute("""
        SELECT nome_atividade, valor, DATE_FORMAT(criado_em, '%d/%m') as data
        FROM portal_notas
        WHERE aluno_id = %s AND criado_em >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        ORDER BY criado_em DESC
        LIMIT 3
    """, (aluno_id,))
    notas = cur.fetchall()

    # Faltas dos últimos 7 dias
    cur.execute("""
        SELECT DATE_FORMAT(data_aula, '%d/%m') as data, t.nome as turma
        FROM portal_chamadas c
        JOIN portal_turmas t ON t.id = c.turma_id
        WHERE c.aluno_id = %s AND c.status = 'F'
        AND data_aula >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        ORDER BY data_aula DESC
        LIMIT 3
    """, (aluno_id,))
    faltas = cur.fetchall()

    # Comunicados dos últimos 7 dias
    cur.execute("""
        SELECT titulo, DATE_FORMAT(criado_em, '%d/%m') as data
        FROM portal_comunicados
        WHERE (tipo = 'aluno' AND aluno_id = %s)
        OR tipo = 'turma'
        AND criado_em >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        ORDER BY criado_em DESC
        LIMIT 3
    """, (aluno_id,))
    comunicados = cur.fetchall()

    cur.close()
    conn.close()

    total = len(notas) + len(faltas) + len(comunicados)
    return jsonify({
        'total': total,
        'notas': notas,
        'faltas': faltas,
        'comunicados': comunicados
    })