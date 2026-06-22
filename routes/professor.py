from flask import Blueprint, render_template, session, redirect, url_for

professor_bp = Blueprint('professor', __name__, url_prefix='/professor')

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorador(*args, **kwargs):
        if session.get('perfil') != 'professor':
            return redirect(url_for('auth.login_professor'))
        return f(*args, **kwargs)
    return decorador

@professor_bp.route('/home')
@login_required
def home():
    return render_template('professor/home.html')

@professor_bp.route('/notas')
@login_required
def notas():
    return render_template('professor/notas/notas.html')

@professor_bp.route('/faltas')
@login_required
def faltas():
    return render_template('professor/faltas/faltas.html')

@professor_bp.route('/comunicados')
@login_required
def comunicados():
    return render_template('professor/comunicados/comunicados.html')

@professor_bp.route('/gerenciamento')
@login_required
def gerenciamento():
    return render_template('professor/gerenciamento/gerenciamento.html')