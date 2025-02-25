from flask import Flask, session, redirect, url_for, request
from flask_session import Session

app = Flask(__name__)

# Set up secret key for encrypting cookies
app.secret_key = '48cb3cfa-50b4-5f42-ab56-7bde3c3cfed5'

# Set up session to store in cookies
app.config['SESSION_TYPE'] = 'filesystem'  # You can use 'redis', 'memcached' if needed

# Initialize session extension
Session(app)

@app.route('/')
def home():
    # Access the session cookie
    if 'username' in session:
        username = session['username']
        return f'Logged in as {username}'
    return 'You are not logged in.'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return '''
    <form method="post">
        <p><input type="text" name="username"></p>
        <p><input type="submit" value="Login"></p>
    </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
