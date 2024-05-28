document.addEventListener("DOMContentLoaded", function () {
    var taskInput = document.getElementById('task');
    var taskList = document.getElementById('taskList');
    var addButton = document.getElementById('addTaskButton');
    var saveButton = document.getElementById('saveTasksButton');
    var moveUpButton = document.getElementById('moveUpButton');
    var moveDownButton = document.getElementById('moveDownButton');
    var selectedIndex = -1; // Инициализируем индекс выбранной задачи
    var importTasksButton = document.getElementById('importTasksButton');

    addButton.addEventListener('click', function () {
        addTask(taskInput, taskList);
    });

    saveButton.addEventListener('click', function () {
        saveTasks(taskList);
    });

    moveUpButton.addEventListener('click', function () {
        moveTaskUp();
    });

    moveDownButton.addEventListener('click', function () {
        moveTaskDown();
    });

    loadTasks(taskList);

    importTasksButton.addEventListener('click', function () {
        var input = document.createElement('input');
        input.type = 'file';

        input.onchange = function (event) {
            var file = event.target.files[0];
            var formData = new FormData();
            formData.append('file', file);

            fetch('/import_tasks', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.tasks) {
                    // Очищаем текущий список задач
                    taskList.innerHTML = '';
                    // Добавляем импортированные задачи в список
                    data.tasks.forEach(task => {
                        var li = document.createElement('li');
                        li.innerHTML = `
                            <span>${task}</span>
                            <button onclick="removeTask(this)">Delete</button>
                        `;
                        li.addEventListener('click', function () {
                            selectTask(li);
                        });
                        taskList.appendChild(li);
                    });
                } else {
                    console.error('Error importing tasks:', data.error);
                }
            })
            .catch(error => {
                console.error('Error importing tasks:', error);
            });
        };

        input.click();
    });
});

function addTask(taskInput, taskList) {
    if (taskInput.value.trim() === '') {
        alert('Please enter a task.');
        return;
    }

    var li = document.createElement('li');
    li.innerHTML = `
        <span>${taskInput.value}</span>
        <button onclick="removeTask(this)">Delete</button>
    `;
    li.addEventListener('click', function () {
        selectTask(li);
    });
    taskList.appendChild(li);

    taskInput.value = '';
}

function removeTask(button) {
    var li = button.parentNode;
    li.parentNode.removeChild(li);
}

function selectTask(li) {
    var taskItems = document.querySelectorAll('#taskList li');
    taskItems.forEach(function (item, index) {
        item.classList.remove('selected');
        if (item === li) {
            selectedIndex = index; // Сохраняем индекс выбранной задачи
        }
    });
    li.classList.add('selected');
}

function moveTaskUp() {
    if (selectedIndex > 0) {
        var currentLi = taskList.children[selectedIndex];
        var previousLi = taskList.children[selectedIndex - 1];
        taskList.insertBefore(currentLi, previousLi);
        selectedIndex--; // Уменьшаем индекс после перемещения вверх
    }
}

function moveTaskDown() {
    if (selectedIndex < taskList.children.length - 1) {
        var currentLi = taskList.children[selectedIndex];
        var nextLi = taskList.children[selectedIndex + 1];
        taskList.insertBefore(nextLi, currentLi);
        selectedIndex++; // Увеличиваем индекс после перемещения вниз
    }
}

function saveTasks(taskList) {
    var tasks = [];
    var taskItems = taskList.getElementsByTagName('li');

    for (var i = 0; i < taskItems.length; i++) {
        var taskText = taskItems[i].getElementsByTagName('span')[0].innerText;
        tasks.push(taskText);
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/save_tasks", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log('Tasks saved successfully!');
                // После успешного сохранения, загружаем обновленный список задач
                loadTasks(taskList);
            } else {
                console.error('Error saving tasks:', xhr.responseText);
            }
        }
    };
    xhr.send(JSON.stringify({ tasks: tasks }));
}

function loadTasks(taskList) {
    fetch('/load_tasks')
        .then(response => response.json())
        .then(data => {
            taskList.innerHTML = '';  // Очищаем текущий список задач

            data.forEach(task => {
                var li = document.createElement('li');
                li.innerHTML = `
                    <span>${task}</span>
                    <button onclick="removeTask(this)">Delete</button>
                `;
                li.addEventListener('click', function () {
                    selectTask(li);
                });
                taskList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error loading tasks:', error);
        });
}
