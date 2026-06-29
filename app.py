import os
from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__)

# Secret key via .env
app.secret_key = os.getenv('SECRET_KEY', 'alfa-portal-secret-2026')

# Sessão expira em 2 horas
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
app.config['SESSION_COOKIE_HTTPONLY']    = True   # JS não acessa o cookie
app.config['SESSION_COOKIE_SAMESITE']   = 'Lax'  # Proteção CSRF básica

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

if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'false').lower() == 'true',
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000))
    )