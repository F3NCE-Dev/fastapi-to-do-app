const form = document.getElementById("form");
const input = document.getElementById("input");
const taskList = document.getElementById("todo-list");

const API_BASE = "http://localhost:8000";

form.addEventListener("submit", addTask);
taskList.addEventListener("click", taskBtnClicking);

document.addEventListener("DOMContentLoaded", loadTasks);

async function loadTasks() {
  const res = await fetch(`${API_BASE}/tasks`);
  const tasks = await res.json();

  taskList.innerHTML = "";

  tasks.forEach(task => renderTask(task));
}


function renderTask(task) {
  const taskHTML = `
    <li class="task ${task.status ? "task-completed" : ""}" data-id="${task.id}">
      <span class="task-text">${task.task}</span>
      <div class="task-btns">
        ${task.status ? "" : `<button id="btn-done" class="btn btn-done">✔️</button>`}
        <button id="btn-remove" class="btn btn-delete">🗑️</button>
      </div>
    </li>
  `;

  taskList.insertAdjacentHTML("beforeend", taskHTML);
}

async function addTask(event) {
  event.preventDefault();
  const taskValue = input.value.trim();
  if (!taskValue) return;

  console.log("Sending task:", taskValue);

  const res = await fetch(`${API_BASE}/add`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      task: taskValue,
      status: false
    })
  });

  if (!res.ok) {
    const errorText = await res.text();
    console.error("Add task failed:", res.status, errorText);
    return;
  }

  await loadTasks();
  input.value = "";
  input.focus();
}

async function taskBtnClicking(event) {
  const li = event.target.closest("li");
  if (!li) return;

  const taskId = li.dataset.id;

  if (event.target.id === "btn-remove") {
    await fetch(`${API_BASE}/remove?task_id=${taskId}`, {
      method: "POST"
    });

    li.remove();
  }

  else if (event.target.id === "btn-done") {
    li.classList.add("task-completed");
    event.target.remove();
  }
}