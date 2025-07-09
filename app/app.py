from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'secret'

# MySQL config
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'orders'

mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1])
    return None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            login_user(User(user[0], username))
            return redirect(url_for('orders'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        product = request.form['product']
        quantity = request.form['quantity']
        cur.execute("INSERT INTO orders (user_id, product, quantity) VALUES (%s, %s, %s)",
                    (current_user.id, product, quantity))
        mysql.connection.commit()
    cur.execute("SELECT id, product, quantity FROM orders WHERE user_id = %s", (current_user.id,))
    order_list = cur.fetchall()
    cur.close()
    return render_template('orders.html', orders=order_list)

@app.route('/delete/<int:order_id>')
@login_required
def delete_order(order_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM orders WHERE id = %s AND user_id = %s", (order_id, current_user.id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('orders'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')