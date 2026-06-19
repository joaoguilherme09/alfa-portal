from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/aluno', methods=['GET', 'POST'])
def login_aluno():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')

        # --- Autenticação provisória (até o banco estar pronto) ---
        # Depois você vai buscar o aluno no banco aqui
        if matricula == '12345' and senha == '123':
            session['usuario'] = matricula
            session['perfil'] = 'aluno'
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.login_aluno'))  # trocar para home do aluno depois
        else:
            flash('Matrícula ou senha incorretos.', 'error')
            return redirect(url_for('auth.login_aluno'))

    return render_template('auth/login_aluno.html')


@auth_bp.route('/login/professor', methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')

        # --- Autenticação provisória (até o banco estar pronto) ---
        # Depois você vai buscar o professor no banco aqui
        if matricula == 'prof01' and senha == '123':
            session['usuario'] = matricula
            session['perfil'] = 'professor'
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.login_professor'))  # trocar para home do professor depois
        else:
            flash('Matrícula ou senha incorretos.', 'error')
            return redirect(url_for('auth.login_professor'))

    return render_template('auth/login_professor.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicial'))