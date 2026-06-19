from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/aluno', methods=['GET', 'POST'])
def login_aluno():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')

        if matricula == '12345' and senha == '123':
            session['perfil'] = 'aluno'
            session['usuario'] = matricula
            session['matricula'] = matricula
            session['nome'] = 'João Guilherme P. Mendes'
            session['curso'] = 'Informática'
            session['periodo'] = 'Manhã'
            session['foto'] = None
            return redirect(url_for('aluno.home'))
        else:
            flash('Matrícula ou senha incorretos.', 'error')
            return redirect(url_for('auth.login_aluno'))

    return render_template('auth/login_aluno.html')


@auth_bp.route('/login/professor', methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')

        if matricula == 'prof01' and senha == '123':
            session['perfil'] = 'professor'
            session['usuario'] = matricula
            session['matricula'] = matricula
            session['nome'] = 'Professor'
            session['foto'] = None
            return redirect(url_for('auth.login_professor'))
        else:
            flash('Matrícula ou senha incorretos.', 'error')
            return redirect(url_for('auth.login_professor'))

    return render_template('auth/login_professor.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicial'))