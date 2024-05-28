from flask import Flask, request, redirect, render_template, jsonify
from models import User 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)


# Создание базы данных
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect('/login')

# Обработчик для страницы входа
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        # Проверка, существует ли пользователь с таким именем в базе данных
        user = User.query.filter_by(username=username).first()
        if user:
            # Пользователь найден, перенаправляем на страницу задач
            return redirect('/tasks')
        else:
            # Пользователь не найден, перенаправляем на страницу регистрации
            return redirect('/registration.html')
    else:
        return render_template('login.html')

# Обработчик для страницы с задачами
@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

# Обработчик для страницы регистрации
@app.route('/registration.html')
def registration():
    return render_template('registration.html')

# Обработчик для регистрации пользователя
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']

    # Проверка, существует ли пользователь с таким именем в базе данных
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        # Если пользователь с таким именем уже существует, вернуть ошибку или выполнить другие действия
        # Например, вы можете перенаправить пользователя на страницу регистрации с сообщением об ошибке
        return redirect('/registration.html')

    # Создание нового пользователя
    new_user = User(username=username)

    # Добавление пользователя в базу данных
    db.session.add(new_user)
    db.session.commit()

    # После успешной регистрации, перенаправляем на страницу задач
    return redirect('/tasks')

# Путь к файлу для хранения задач
TASKS_FILE = 'tasks/tasks.txt'

@app.route('/save_tasks', methods=['POST'])
def save_tasks():
    # Получаем данные задач из POST-запроса
    tasks = request.json.get('tasks', [])

    # Сохраняем задачи в файл
    with open(TASKS_FILE, 'w') as f:
        for task in tasks:
            f.write(task + '\n')

    # Возвращаем подтверждение об успешном сохранении
    return jsonify({'message': 'Tasks saved successfully!'})


@app.route('/load_tasks', methods=['GET'])
def load_tasks():
    # Ваши действия по загрузке задач, например, чтение из базы данных
    tasks = ['Task 1', 'Task 2', 'Task 3']  # Пример загруженных задач
    print('Loaded tasks:', tasks)
    # Возвращаем список задач в формате JSON
    return jsonify(tasks), 200

# Маршрут для просмотра всех пользователей
@app.route('/users')
def view_users():
    users = User.query.all()  # Получение всех пользователей из базы данных
    user_list = [user.username for user in users]  # Создание списка имен пользователей
    return jsonify(user_list)  # Возвращение списка в формате JSON


if __name__ == '__main__':
    app.run(debug=True)
