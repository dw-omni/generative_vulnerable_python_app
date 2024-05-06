from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib  # Dodane do wygenerowania niezabezpieczonego skrótu hasła

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model użytkownika
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Inicjalizacja bazy danych
db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Podatność: Użycie niebezpiecznej funkcji skrótu (MD5)
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Registration successful!', 'success')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Podatność: Brak uwierzytelniania i autoryzacji
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['logged_in'] = True
        session['username'] = username
        flash('Login successful!', 'success')
    else:
        flash('Invalid username or password!', 'error')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)  # Podatność: Użycie trybu debugowania w aplikacji produkcyjnej
