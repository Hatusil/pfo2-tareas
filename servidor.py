from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configuración de la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'usuarios.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(150), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)

# Crear las tablas
with app.app_context():
    db.create_all()

# Ruta para registrar un usuario
@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')

    if Usuario.query.filter_by(usuario=usuario).first():
        return jsonify({"mensaje": "Usuario ya existe"}), 400

    hash_contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    nuevo_usuario = Usuario(usuario=usuario, contrasena=hash_contrasena)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado con éxito"}), 201

# Ruta para login
@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')

    user = Usuario.query.filter_by(usuario=usuario).first()
    if user and bcrypt.check_password_hash(user.contrasena, contrasena):
        return redirect('/tareas')
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

# Página de bienvenida
@app.route('/tareas', methods=['GET'])
def tareas():
    return render_template('bienvenida.html')

if __name__ == '__main__':
    app.run(debug=True)
