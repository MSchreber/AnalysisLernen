from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
SHARE_FOLDER = '/path/to/share'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('explorer'))
        return 'Login failed', 403
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

@app.route('/explorer', defaults={'path': ''})
@app.route('/explorer/<path:path>')
def explorer(path):
    if not session.get('admin'):
        return redirect(url_for('login'))

    abs_path = os.path.join(SHARE_FOLDER, path)
    if not os.path.exists(abs_path):
        return 'Path not found', 404

    if os.path.isfile(abs_path):
        return send_from_directory(SHARE_FOLDER, path, as_attachment=True)

    files = os.listdir(abs_path)
    return render_template('explorer.html', files=files, current_path=path)

if __name__ == '__main__':
    app.run(debug=True)
