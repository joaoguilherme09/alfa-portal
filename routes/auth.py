from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import create_connection, get_cursor
from crypto import verificar_senha, descriptografar

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/aluno', methods=['GET', 'POST'])
def login_aluno():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha     = request.form.get('senha')

        conn = create_connection()
        cur  = get_cursor(conn)
        cur.execute("""
            SELECT id, nome, matricula, senha, periodo, foto
            FROM portal_alunos WHERE matricula = %s
        """, (matricula,))
        aluno = cur.fetchone()

        if aluno and verificar_senha(senha, aluno['senha']):
            cur.execute("""
                SELECT DISTINCT c.nome as curso
                FROM portal_aluno_turma at2
                JOIN portal_turmas t ON t.id = at2.turma_id
                JOIN portal_cursos c ON c.id = t.curso_id
                WHERE at2.aluno_id = %s
            """, (aluno['id'],))
            cursos_raw = cur.fetchall()
            cur.close()
            conn.close()

            cursos_str = ' + '.join([c['curso'] for c in cursos_raw]) if cursos_raw else '—'

            session['perfil']    = 'aluno'
            session['id']        = aluno['id']
            session['nome']      = aluno['nome']
            session['matricula'] = aluno['matricula']
            session['periodo']   = aluno['periodo']
            session['foto']      = aluno['foto']
            session['curso']     = cursos_str
            return redirect(url_for('aluno.home'))
        else:
            cur.close()
            conn.close()
            flash('Matrícula ou senha incorretos.', 'error')
            return redirect(url_for('auth.login_aluno'))

    return render_template('auth/login_aluno.html')


@auth_bp.route('/login/professor', methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha     = request.form.get('senha')

        conn = create_connection()
        cur  = get_cursor(conn)
        cur.execute("""
            SELECT id, nome, matricula, senha, cargo, foto
            FROM portal_professores WHERE matricula = %s
        """, (matricula,))
        professor = cur.fetchone()
        cur.close()
        conn.close()

        if professor and verificar_senha(senha, professor['senha']):
            session['perfil']    = 'professor'
            session['id']        = professor['id']
            session['nome']      = professor['nome']
            session['matricula'] = professor['matricula']
            session['cargo']     = professor['cargo'].capitalize()
            session['foto']      = professor['foto']
            return redirect(url_for('professor.home'))
        else:
            flash('Matrícula ou senha incorretos.', 'error')
            return redirect(url_for('auth.login_professor'))

    return render_template('auth/login_professor.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicial'))