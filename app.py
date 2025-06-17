from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Créer la base s'il faut
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Nom d'utilisateur déjà pris"
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        if result and check_password_hash(result[0], password):
            session['user'] = username
            return redirect('/chat')
            
        else:
            return "Échec de la connexion"
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/login')
    return "Bienvenue dans le chat!"

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
