from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Inicjalizacja bazy danych
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Podatność: Brak sanityzacji danych wejściowych
    c.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
