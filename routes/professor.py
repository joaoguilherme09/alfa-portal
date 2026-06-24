from flask import Blueprint, render_template, session, redirect, url_for
from db import create_connection, get_cursor
from datetime import date

professor_bp = Blueprint('professor', __name__, url_prefix='/professor')

NOMES_MESES = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
}

DIAS_PT = {
    'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
    'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
}

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorador(*args, **kwargs):
        if session.get('perfil') != 'professor':
            return redirect(url_for('auth.login_professor'))
        return f(*args, **kwargs)
    return decorador


def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorador(*args, **kwargs):
        if session.get('perfil') != 'professor':
            return redirect(url_for('auth.login_professor'))
        if session.get('cargo', '').lower() != 'admin':
            return redirect(url_for('professor.home'))
        return f(*args, **kwargs)
    return decorador


@professor_bp.route('/home')
@login_required
def home():
    professor_id = session['id']
    hoje = date.today()
    dia_semana_en = hoje.strftime('%A')
    dia_semana_pt = DIAS_PT.get(dia_semana_en, '')

    conn = create_connection()
    cur  = get_cursor(conn)

    # Turmas do professor
    cur.execute("""
        SELECT t.id, t.nome, t.dias_semana, t.horario, c.nome as curso
        FROM portal_turmas t
        JOIN portal_cursos c ON c.id = t.curso_id
        WHERE t.professor_id = %s
    """, (professor_id,))
    todas_turmas = cur.fetchall()

    # Turmas de hoje
    turmas_hoje = [t for t in todas_turmas if dia_semana_pt in t['dias_semana']]

    # Total de notas lançadas hoje
    cur.execute("""
        SELECT COUNT(*) as qtd FROM portal_notas
        WHERE professor_id = %s AND DATE(criado_em) = %s
    """, (professor_id, hoje))
    notas_hoje = cur.fetchone()['qtd']

    # Total de comunicados enviados hoje
    cur.execute("""
        SELECT COUNT(*) as qtd FROM portal_comunicados
        WHERE professor_id = %s AND DATE(criado_em) = %s
    """, (professor_id, hoje))
    comunicados_hoje = cur.fetchone()['qtd']

    cur.close()
    conn.close()

    return render_template('professor/home.html',
        turmas_hoje=turmas_hoje,
        total_turmas=len(todas_turmas),
        notas_hoje=notas_hoje,
        comunicados_hoje=comunicados_hoje
    )

@professor_bp.route('/notas')
@login_required
def notas():
    professor_id = session['id']
    conn = create_connection()
    cur  = get_cursor(conn)

    cur.execute("""
        SELECT t.id, t.nome, c.nome as curso
        FROM portal_turmas t
        JOIN portal_cursos c ON c.id = t.curso_id
        WHERE t.professor_id = %s
    """, (professor_id,))
    turmas = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('professor/notas/notas.html',
        turmas=turmas,
        nomes_meses=NOMES_MESES
    )

@professor_bp.route('/faltas')
@login_required
def faltas():
    professor_id = session['id']
    conn = create_connection()
    cur  = get_cursor(conn)

    cur.execute("""
        SELECT t.id, t.nome, t.dias_semana, t.horario, c.nome as curso
        FROM portal_turmas t
        JOIN portal_cursos c ON c.id = t.curso_id
        WHERE t.professor_id = %s
    """, (professor_id,))
    turmas = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('professor/faltas/faltas.html', turmas=turmas)

@professor_bp.route('/faltas/alunos/<int:turma_id>')
@login_required
def faltas_alunos(turma_id):
    professor_id = session['id']
    hoje = date.today()

    conn = create_connection()
    cur  = get_cursor(conn)

    # Dados da turma
    cur.execute("""
        SELECT t.nome, t.horario, c.nome as curso
        FROM portal_turmas t
        JOIN portal_cursos c ON c.id = t.curso_id
        WHERE t.id = %s
    """, (turma_id,))
    turma = cur.fetchone()

    # Alunos da turma
    cur.execute("""
        SELECT a.id, a.nome, a.foto,
            (SELECT COUNT(*) FROM portal_chamadas
             WHERE aluno_id = a.id AND turma_id = %s
             AND status = 'F' AND MONTH(data_aula) = MONTH(NOW())) as faltas_mes
        FROM portal_aluno_turma at2
        JOIN portal_alunos a ON a.id = at2.aluno_id
        WHERE at2.turma_id = %s
    """, (turma_id, turma_id))
    alunos = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('professor/faltas/chamada.html',
        turma=turma,
        turma_id=turma_id,
        alunos=alunos,
        hoje=hoje.strftime('%d/%m/%Y')
    )

@professor_bp.route('/comunicados')
@login_required
def comunicados():
    professor_id = session['id']
    conn = create_connection()
    cur  = get_cursor(conn)

    cur.execute("""
        SELECT titulo, arquivo, tipo, DATE_FORMAT(criado_em, '%d/%m/%Y') as data
        FROM portal_comunicados
        WHERE professor_id = %s
        ORDER BY criado_em DESC
    """, (professor_id,))
    comunicados = cur.fetchall()

    cur.execute("""
        SELECT t.id, t.nome, c.nome as curso
        FROM portal_turmas t
        JOIN portal_cursos c ON c.id = t.curso_id
        WHERE t.professor_id = %s
    """, (professor_id,))
    turmas = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('professor/comunicados/comunicados.html',
        comunicados=comunicados,
        turmas=turmas
    )

@professor_bp.route('/gerenciamento')
@admin_required
def gerenciamento():
    conn = create_connection()
    cur  = get_cursor(conn)

    cur.execute("SELECT * FROM portal_cursos")
    cursos = cur.fetchall()

    cur.execute("""
        SELECT t.*, c.nome as curso, p.nome as professor
        FROM portal_turmas t
        JOIN portal_cursos c ON c.id = t.curso_id
        JOIN portal_professores p ON p.id = t.professor_id
    """)
    turmas = cur.fetchall()

    cur.execute("SELECT id, nome, matricula, cargo FROM portal_professores")
    professores = cur.fetchall()

    cur.execute("""
        SELECT a.id, a.nome, a.matricula,
            MAX(c.nome) as curso
        FROM portal_alunos a
        LEFT JOIN portal_aluno_turma at2 ON at2.aluno_id = a.id
        LEFT JOIN portal_turmas t ON t.id = at2.turma_id
        LEFT JOIN portal_cursos c ON c.id = t.curso_id
        GROUP BY a.id, a.nome, a.matricula
    """)
    alunos = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('professor/gerenciamento/gerenciamento.html',
        cursos=cursos,
        turmas=turmas,
        professores=professores,
        alunos=alunos
    )

from flask import jsonify, request as flask_request
import datetime

@professor_bp.route('/alunos_turma/<int:turma_id>')
@login_required
def alunos_turma(turma_id):
    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        SELECT a.id, a.nome
        FROM portal_aluno_turma at2
        JOIN portal_alunos a ON a.id = at2.aluno_id
        WHERE at2.turma_id = %s
        ORDER BY a.nome
    """, (turma_id,))
    alunos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(alunos)

@professor_bp.route('/salvar_nota', methods=['POST'])
@login_required
def salvar_nota():
    professor_id = session['id']
    data = flask_request.get_json()

    try:
        conn = create_connection()
        cur  = get_cursor(conn)
        cur.execute("""
            INSERT INTO portal_notas
            (aluno_id, turma_id, professor_id, nome_atividade, mes, ano, valor)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['aluno_id'],
            data['turma_id'],
            professor_id,
            data['atividade'],
            data['mes'],
            datetime.date.today().year,
            data['nota']
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'erro': str(e)})

@professor_bp.route('/salvar_chamada', methods=['POST'])
@login_required
def salvar_chamada():
    professor_id = session['id']
    data = flask_request.get_json()
    turma_id = data['turma_id']
    status_alunos = data['status']
    hoje = data['data']

    try:
        conn = create_connection()
        cur  = get_cursor(conn)
        for aluno_id, status in status_alunos.items():
            cur.execute("""
                INSERT INTO portal_chamadas
                (aluno_id, turma_id, professor_id, data_aula, status)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """, (aluno_id, turma_id, professor_id, hoje, status))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'erro': str(e)})

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/comunicados'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@professor_bp.route('/salvar_comunicado', methods=['POST'])
@login_required
def salvar_comunicado():
    from flask import current_app
    professor_id = session['id']
    titulo    = flask_request.form.get('titulo')
    tipo      = flask_request.form.get('tipo')
    turma_id  = flask_request.form.get('turma_id') or None
    aluno_id  = flask_request.form.get('aluno_id') or None
    arquivo   = flask_request.files.get('arquivo')

    if arquivo and allowed_file(arquivo.filename):
        filename = secure_filename(arquivo.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        arquivo.save(os.path.join(UPLOAD_FOLDER, filename))

        conn = create_connection()
        cur  = get_cursor(conn)
        cur.execute("""
            INSERT INTO portal_comunicados
            (professor_id, titulo, arquivo, tipo, turma_id, aluno_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (professor_id, titulo, filename, tipo, turma_id, aluno_id))
        conn.commit()
        cur.close()
        conn.close()

    return redirect(url_for('professor.comunicados'))

@professor_bp.route('/salvar_turma', methods=['POST'])
@login_required
def salvar_turma():
    nome         = flask_request.form.get('nome')
    curso_id     = flask_request.form.get('curso_id')
    professor_id = flask_request.form.get('professor_id')
    dias         = ','.join(flask_request.form.getlist('dias'))
    horario      = flask_request.form.get('horario')
    periodo      = flask_request.form.get('periodo')

    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        INSERT INTO portal_turmas (nome, curso_id, professor_id, dias_semana, horario, periodo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nome, curso_id, professor_id, dias, horario, periodo))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('professor.gerenciamento'))

@professor_bp.route('/salvar_professor', methods=['POST'])
@login_required
def salvar_professor():
    nome      = flask_request.form.get('nome')
    matricula = flask_request.form.get('matricula')
    senha     = flask_request.form.get('senha')
    cargo     = flask_request.form.get('cargo')

    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        INSERT INTO portal_professores (nome, matricula, senha, cargo)
        VALUES (%s, %s, %s, %s)
    """, (nome, matricula, senha, cargo))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('professor.gerenciamento'))
 
@professor_bp.route('/salvar_aluno', methods=['POST'])
@login_required
def salvar_aluno():
    f        = flask_request.form
    turmas   = flask_request.form.getlist('turmas[]')
 
    conn = create_connection()
    cur  = get_cursor(conn)
 
    # Gerar matrícula automática
    cur.execute("SELECT MAX(CAST(matricula AS UNSIGNED)) as max_mat FROM portal_alunos")
    resultado    = cur.fetchone()
    nova_matricula = str((resultado['max_mat'] or 50240000) + 1)
 
    cur.execute("""
        INSERT INTO portal_alunos (
            nome_responsavel, nascimento_responsavel, cpf_responsavel,
            rg_responsavel, telefone_responsavel,
            nome, nascimento, endereco, bairro, numero, cidade, cep,
            matricula, senha, periodo
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        f['nome_responsavel'], f['nascimento_responsavel'], f['cpf_responsavel'],
        f['rg_responsavel'], f['telefone_responsavel'],
        f['nome'], f['nascimento'], f['endereco'], f['bairro'],
        f['numero'], f['cidade'], f['cep'],
        nova_matricula, f['senha'], f['periodo']
    ))
    aluno_id = cur.lastrowid
 
    # Vincular às turmas selecionadas
    for turma_id in turmas:
        cur.execute("""
            INSERT INTO portal_aluno_turma (aluno_id, turma_id)
            VALUES (%s, %s)
        """, (aluno_id, turma_id))
 
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('professor.gerenciamento'))
 

import os
from docxtpl import DocxTemplate

@professor_bp.route('/salvar_matricula', methods=['POST'])
@login_required
def salvar_matricula():
    f = flask_request.form
    aluno_id = f['aluno_id']

    conn = create_connection()
    cur  = get_cursor(conn)

    # Buscar dados do aluno
    cur.execute("SELECT * FROM portal_alunos WHERE id = %s", (aluno_id,))
    aluno = cur.fetchone()

    # Buscar turma do aluno para pegar dia e horário
    cur.execute("""
        SELECT t.dias_semana, t.horario
        FROM portal_aluno_turma at2
        JOIN portal_turmas t ON t.id = at2.turma_id
        WHERE at2.aluno_id = %s LIMIT 1
    """, (aluno_id,))
    turma = cur.fetchone()

    # Próximo número de contrato (se não digitado)
    numero_contrato = f.get('numero_contrato')
    if not numero_contrato:
        cur.execute("SELECT MAX(numero_contrato) as max_num FROM portal_matriculas_contratos")
        resultado = cur.fetchone()
        numero_contrato = (resultado['max_num'] or 0) + 1

    # Parcelas por extenso automático
    extenso_map = {'6': 'SEIS', '12': 'DOZE', '18': 'DEZOITO'}
    parcelas_extenso = extenso_map.get(str(f['qtd_parcelas']), f['qtd_parcelas'])

    dia_horario = f'{turma["dias_semana"]} {turma["horario"]}' if turma else '—'

    # Salvar no banco
    cur.execute("""
        INSERT INTO portal_matriculas_contratos (
            aluno_id, numero_contrato, data_matricula, data_primeiro_pagamento,
            curso_contrato, modulo, preco_total, qtd_parcelas,
            parcelas_extenso, valor_parcela, dia_horario
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        aluno_id, numero_contrato, f['data_matricula'],
        f['data_primeiro_pagamento'], f['curso_contrato'], f['modulo'],
        f['preco_total'], f['qtd_parcelas'], parcelas_extenso,
        f['valor_parcela'], dia_horario
    ))
    conn.commit()

    # Formatar datas para o contrato (dd/mm/aaaa)
    def fmt_data(d):
        if not d: return ''
        partes = str(d).split('-')
        if len(partes) == 3:
            return f"{partes[2]}/{partes[1]}/{partes[0]}"
        return str(d)

    # Preencher o modelo com docxtpl
    modelo_path = os.path.join('contrato', 'modelo-contrato.docx')
    doc = DocxTemplate(modelo_path)

    contexto = {
        'numero_contrato':         str(numero_contrato),
        'nome_responsavel':        aluno['nome_responsavel'],
        'nascimento_responsavel':  fmt_data(aluno['nascimento_responsavel']),
        'cpf_responsavel':         aluno['cpf_responsavel'],
        'rg_responsavel':          aluno['rg_responsavel'],
        'telefone_responsavel':    aluno['telefone_responsavel'],
        'nome_aluno':              aluno['nome'],
        'nascimento_aluno':        fmt_data(aluno['nascimento']),
        'endereco':                aluno['endereco'],
        'bairro':                  aluno['bairro'],
        'numero':                  aluno['numero'],
        'cep':                     aluno['cep'],
        'data_matricula':          fmt_data(f['data_matricula']),
        'data_primeiro_pagamento': fmt_data(f['data_primeiro_pagamento']),
        'curso_contrato':          f['curso_contrato'],
        'modulo':                  f['modulo'],
        'preco_total':             f['preco_total'],
        'qtd_parcelas':            f['qtd_parcelas'],
        'parcelas_extenso':        parcelas_extenso,
        'valor_parcela':           f['valor_parcela'],
        'dia_horario':             dia_horario,
    }

    doc.render(contexto)

    # Salvar o docx preenchido
    os.makedirs('uploads/contratos', exist_ok=True)
    nome_arquivo = f"contrato_{numero_contrato}_{aluno_id}.docx"
    caminho_docx = os.path.join('uploads', 'contratos', nome_arquivo)
    doc.save(caminho_docx)

    # Atualizar arquivo gerado no banco
    cur.execute("""
        UPDATE portal_matriculas_contratos SET arquivo_gerado = %s
        WHERE aluno_id = %s AND numero_contrato = %s
    """, (nome_arquivo, aluno_id, numero_contrato))
    conn.commit()
    cur.close()
    conn.close()

    # Baixar o arquivo
    from flask import send_file
    return send_file(
        caminho_docx,
        as_attachment=True,
        download_name=f"Contrato_{aluno['nome']}.docx"
    )


@professor_bp.route('/buscar_aluno/<int:aluno_id>')
@login_required
def buscar_aluno(aluno_id):
    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("SELECT * FROM portal_alunos WHERE id = %s", (aluno_id,))
    aluno = cur.fetchone()
 
    # Buscar TODAS as turmas do aluno
    cur.execute("""
        SELECT turma_id FROM portal_aluno_turma WHERE aluno_id = %s
    """, (aluno_id,))
    turmas = [t['turma_id'] for t in cur.fetchall()]
    cur.close()
    conn.close()
 
    if aluno:
        aluno['nascimento']             = str(aluno['nascimento'])
        aluno['nascimento_responsavel'] = str(aluno['nascimento_responsavel'])
        aluno['turmas']                 = turmas
        return jsonify(aluno)
    return jsonify({'erro': 'Aluno não encontrado'}), 404
 
 
@professor_bp.route('/editar_aluno', methods=['POST'])
@login_required
def editar_aluno():
    f        = flask_request.form
    aluno_id = f['aluno_id']
    turmas   = flask_request.form.getlist('turmas[]')
 
    conn = create_connection()
    cur  = get_cursor(conn)
 
    cur.execute("""
        UPDATE portal_alunos SET
            nome_responsavel = %s, nascimento_responsavel = %s,
            cpf_responsavel = %s, rg_responsavel = %s, telefone_responsavel = %s,
            nome = %s, nascimento = %s, endereco = %s, bairro = %s,
            numero = %s, cidade = %s, cep = %s, periodo = %s, senha = %s
        WHERE id = %s
    """, (
        f['nome_responsavel'], f['nascimento_responsavel'],
        f['cpf_responsavel'], f['rg_responsavel'], f['telefone_responsavel'],
        f['nome'], f['nascimento'], f['endereco'], f['bairro'],
        f['numero'], f['cidade'], f['cep'], f['periodo'], f['senha'],
        aluno_id
    ))
 
    # Atualizar turmas — apaga todas e recadastra
    cur.execute("DELETE FROM portal_aluno_turma WHERE aluno_id = %s", (aluno_id,))
    for turma_id in turmas:
        cur.execute("""
            INSERT INTO portal_aluno_turma (aluno_id, turma_id)
            VALUES (%s, %s)
        """, (aluno_id, turma_id))
 
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('professor.gerenciamento'))
 

@professor_bp.route('/buscar_professor/<int:professor_id>')
@login_required
def buscar_professor(professor_id):
    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("SELECT id, nome, matricula, cargo FROM portal_professores WHERE id = %s", (professor_id,))
    professor = cur.fetchone()
    cur.close()
    conn.close()
    if professor:
        return jsonify(professor)
    return jsonify({'erro': 'Professor não encontrado'}), 404

@professor_bp.route('/editar_professor', methods=['POST'])
@login_required
def editar_professor():
    f = flask_request.form
    professor_id = f['professor_id']

    conn = create_connection()
    cur  = get_cursor(conn)

    if f.get('senha'):
        cur.execute("""
            UPDATE portal_professores
            SET nome = %s, matricula = %s, cargo = %s, senha = %s
            WHERE id = %s
        """, (f['nome'], f['matricula'], f['cargo'], f['senha'], professor_id))
    else:
        cur.execute("""
            UPDATE portal_professores
            SET nome = %s, matricula = %s, cargo = %s
            WHERE id = %s
        """, (f['nome'], f['matricula'], f['cargo'], professor_id))

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('professor.gerenciamento'))



@professor_bp.route('/buscar_turma/<int:turma_id>')
@login_required
def buscar_turma(turma_id):
    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        SELECT t.id, t.nome, t.curso_id, t.professor_id,
               t.dias_semana, t.horario, t.periodo
        FROM portal_turmas t
        WHERE t.id = %s
    """, (turma_id,))
    turma = cur.fetchone()
    cur.close()
    conn.close()
    if turma:
        return jsonify(turma)
    return jsonify({'erro': 'Turma não encontrada'}), 404

@professor_bp.route('/editar_turma', methods=['POST'])
@login_required
def editar_turma():
    f = flask_request.form
    turma_id = f['turma_id']
    dias = ','.join(flask_request.form.getlist('dias'))

    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        UPDATE portal_turmas
        SET nome = %s, curso_id = %s, professor_id = %s,
            dias_semana = %s, horario = %s, periodo = %s
        WHERE id = %s
    """, (
        f['nome'], f['curso_id'], f['professor_id'],
        dias, f['horario'], f['periodo'],
        turma_id
    ))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('professor.gerenciamento'))


# Adicione essas rotas no routes/professor.py

@professor_bp.route('/chamadas_mes/<int:turma_id>/<int:ano>/<int:mes>')
@login_required
def chamadas_mes(turma_id, ano, mes):
    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        SELECT DISTINCT DATE_FORMAT(data_aula, '%Y-%m-%d') as data_aula
        FROM portal_chamadas
        WHERE turma_id = %s
          AND YEAR(data_aula) = %s
          AND MONTH(data_aula) = %s
    """, (turma_id, ano, mes))
    chamadas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(chamadas)

@professor_bp.route('/alunos_chamada/<int:turma_id>/<string:data>')
@login_required
def alunos_chamada(turma_id, data):
    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        SELECT a.id, a.nome,
            COALESCE(
                (SELECT status FROM portal_chamadas
                 WHERE aluno_id = a.id AND turma_id = %s AND data_aula = %s),
                'P'
            ) as status,
            (SELECT COUNT(*) FROM portal_chamadas
             WHERE aluno_id = a.id AND turma_id = %s
             AND status = 'F' AND MONTH(data_aula) = MONTH(%s)) as faltas_mes
        FROM portal_aluno_turma at2
        JOIN portal_alunos a ON a.id = at2.aluno_id
        WHERE at2.turma_id = %s
        ORDER BY a.nome
    """, (turma_id, data, turma_id, data, turma_id))
    alunos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(alunos)


# Adicione essas rotas no routes/professor.py

@professor_bp.route('/curso/<int:curso_id>/turmas')
@admin_required
def curso_turmas(curso_id):
    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("SELECT nome FROM portal_cursos WHERE id = %s", (curso_id,))
    curso = cur.fetchone()
    cur.execute("""
        SELECT t.id, t.nome, t.dias_semana, t.horario, t.periodo,
               p.nome as professor,
               (SELECT COUNT(*) FROM portal_aluno_turma WHERE turma_id = t.id) as total_alunos
        FROM portal_turmas t
        JOIN portal_professores p ON p.id = t.professor_id
        WHERE t.curso_id = %s
    """, (curso_id,))
    turmas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('professor/gerenciamento/curso_turmas.html',
        curso=curso, turmas=turmas, curso_id=curso_id)

@professor_bp.route('/turma/<int:turma_id>/alunos')
@admin_required
def turma_alunos(turma_id):
    conn = create_connection()
    cur  = get_cursor(conn)
    cur.execute("""
        SELECT t.nome as turma, c.nome as curso
        FROM portal_turmas t
        JOIN portal_cursos c ON c.id = t.curso_id
        WHERE t.id = %s
    """, (turma_id,))
    turma = cur.fetchone()
    cur.execute("""
        SELECT a.id, a.nome, a.matricula, a.periodo,
               (SELECT COUNT(*) FROM portal_chamadas
                WHERE aluno_id = a.id AND turma_id = %s
                AND status = 'F' AND MONTH(data_aula) = MONTH(NOW())) as faltas_mes
        FROM portal_aluno_turma at2
        JOIN portal_alunos a ON a.id = at2.aluno_id
        WHERE at2.turma_id = %s
        ORDER BY a.nome
    """, (turma_id, turma_id))
    alunos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('professor/gerenciamento/turma_alunos.html',
        turma=turma, alunos=alunos, turma_id=turma_id)