from flask import Blueprint, render_template, session, redirect, url_for

aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')

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
    return render_template('aluno/notas.html')

@aluno_bp.route('/faltas')
@login_required
def faltas():
    return render_template('aluno/faltas.html')

@aluno_bp.route('/comentarios')
@login_required
def comentarios():
    return render_template('aluno/comentarios.html')