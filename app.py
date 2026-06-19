from flask import Flask, render_template
from routes.auth import auth_bp

app = Flask(__name__)
app.secret_key = 'alfa-portal-secret-2026'  # troque por uma chave segura depois

# Registrar blueprints
app.register_blueprint(auth_bp)

@app.route('/')
def inicial():
    return render_template('inicial.html')

if __name__ == '__main__':
    app.run(debug=True)