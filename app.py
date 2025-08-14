
# User Management System - Flask App
# Setup: python -m venv venv && source venv/bin/activate && pip install flask flask_sqlalchemy

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    db.session.add(User(name=name, email=email, password=password))
    db.session.commit()
    flash('User added successfully!')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    user.name = request.form['name']
    user.email = request.form['email']
    user.password = request.form['password']
    db.session.commit()
    flash('User updated successfully!')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!')
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
