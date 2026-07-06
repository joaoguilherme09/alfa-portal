import os
from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)

# Secret key via .env
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise ValueError("SECRET_KEY não definida!")
app.secret_key = secret_key

# Sessão
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['SESSION_COOKIE_HTTPONLY']    = True
app.config['SESSION_COOKIE_SAMESITE']   = 'Lax'

# Rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5000 per day", "1000 per hour"]
)

# Headers de segurança
@app.after_request
def security_headers(response):
    response.headers['X-Frame-Options']       = 'SAMEORIGIN'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection']       = '1; mode=block'
    response.headers['Referrer-Policy']         = 'strict-origin-when-cross-origin'
    return response

# Blueprints
from routes.auth      import auth_bp
from routes.aluno     import aluno_bp
from routes.professor import professor_bp

app.register_blueprint(auth_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(professor_bp)

# Rotas
@app.route('/')
def inicial():
    return render_template('inicial.html')

# Páginas de erro
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template('500.html'), 500

@app.errorhandler(429)
def rate_limit_excedido(e):
    return render_template('429.html'), 429

if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )
