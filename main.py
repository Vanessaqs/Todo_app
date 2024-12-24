from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lugares.sqlite'
db = SQLAlchemy(app)

# Modelo de la base de datos
class Lugar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # Nacional o Internacional
    visitado = db.Column(db.String(3), nullable=False, default="No")  # Sí o No

# Crear la base de datos
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    lugares = Lugar.query.all()
    return render_template('index.html', lugares=lugares)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    tipo = request.form.get('tipo')

    nuevo_lugar = Lugar(nombre=nombre, tipo=tipo, visitado="No")
    db.session.add(nuevo_lugar)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/confirmar/<int:id>', methods=['POST'])
def confirmar(id):
    lugar = Lugar.query.get(id)
    if lugar:
        lugar.visitado = "No" if lugar.visitado == "Sí" else "Sí"
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    lugar = Lugar.query.get(id)
    if lugar:
        db.session.delete(lugar)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
