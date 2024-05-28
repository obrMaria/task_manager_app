from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(100), nullable=False)

# Создание базы данных
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            Task.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            return redirect('/tasks')
        else:
            error_message = 'User not found. Please try again.'
            return render_template('login.html', error=error_message)
    else:
        return render_template('login.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/registration.html')
def registration():
    error = request.args.get('error')
    return render_template('registration.html', error=error)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return redirect('/registration.html?error=User already exists')
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/tasks')

# Путь к файлу для хранения задач
TASKS_FILE = 'tasks/tasks.txt'

@app.route('/save_tasks', methods=['POST'])
def save_tasks():
    # Получаем данные задач из POST-запроса
    tasks = request.json.get('tasks', [])

    # Очищаем файл с задачами перед записью новых
    with open(TASKS_FILE, 'w') as f:
        for task in tasks:
            f.write(task + '\n')

    # Возвращаем подтверждение об успешном сохранении
    return jsonify({'message': 'Tasks saved successfully!'})

@app.route('/load_tasks', methods=['GET'])
def load_tasks():
    # Читаем задачи из файла
    with open(TASKS_FILE, 'r') as f:
        tasks = [line.strip() for line in f.readlines()]
    return jsonify(tasks), 200

@app.route('/import_tasks', methods=['POST'])
def import_tasks():
    file = request.files['file']
    if file:
        tasks = file.read().decode('utf-8').splitlines()
        clear_all_tasks()
        user = User.query.first()
        if user:
            for task_description in tasks:
                new_task = Task(user_id=user.id, description=task_description)
                db.session.add(new_task)
            db.session.commit()
            # Получаем все задачи для пользователя после импорта
            user_tasks = Task.query.filter_by(user_id=user.id).all()
            task_list = [task.description for task in user_tasks]
            return jsonify({'tasks': task_list}), 200
        else:
            return jsonify({'error': 'No user found to assign tasks'}), 500
    else:
        return jsonify({'error': 'No file was uploaded'}), 400

def clear_all_tasks():
    Task.query.delete()
    db.session.commit()

# возможности администратора
# Маршрут для просмотра всех пользователей
@app.route('/users')
def view_users():
    users = User.query.all()  # Получение всех пользователей из базы данных
    user_list = [user.username for user in users]  # Создание списка имен пользователей
    return jsonify(user_list)  # Возвращение списка в формате JSON

# Маршрут для пудаление всех пользователей
@app.route('/clear_users', methods=['GET', 'POST'])
def clear_users():
    if request.method == 'POST':
        # Удаляем всех пользователей из базы данных
        db.session.query(User).delete()
        db.session.commit()
        return jsonify({'message': 'User list cleared successfully!'})
    elif request.method == 'GET':
        # Возвращаем страницу с формой подтверждения очистки пользователей
        return render_template('clear_users.html')

if __name__ == '__main__':
    app.run(debug=True)