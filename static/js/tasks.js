// 2.js
document.addEventListener("DOMContentLoaded", function () {
    var taskInput = document.getElementById('task');
    var taskList = document.getElementById('taskList');
    var addButton = document.getElementById('addTaskButton');
    var saveButton = document.getElementById('saveTasksButton'); // Добавленная кнопка

    addButton.addEventListener('click', function () {
        addTask(taskInput, taskList);
    });

    saveButton.addEventListener('click', function () {
        saveTasks(taskList);
    });

    // Загрузка задач из сохраненных данных (вызывается при загрузке страницы)
    loadTasks(taskList);
});

function addTask(taskInput, taskList) {
    if (taskInput.value.trim() === '') {
        alert('Please enter a task.');
        return;
    }

    var li = document.createElement('li');
    li.innerHTML = '<span>' + taskInput.value + '</span><button onclick="removeTask(this)">Delete</button>';
    taskList.appendChild(li);

    taskInput.value = '';
}

function removeTask(button) {
    var li = button.parentNode;
    li.parentNode.removeChild(li);
}

function saveTasks(taskList) {
    var tasks = [];
    var taskItems = taskList.getElementsByTagName('li');

    for (var i = 0; i < taskItems.length; i++) {
        var taskText = taskItems[i].getElementsByTagName('span')[0].innerText;
        tasks.push(taskText);
    }

    // Отправляем данные о задачах на сервер
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/save_tasks", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log('Tasks saved successfully!');
            } else {
                console.error('Error saving tasks:', xhr.responseText);
            }
        }
    };
    xhr.send(JSON.stringify({ tasks: tasks }));
}


function loadTasks(taskList) {
    // Загрузка задач из сохраненных данных, здесь вы можете добавить логику загрузки с сервера или из локального хранилища
    console.log('Tasks loaded successfully!');
}
