import json
from flask import Flask, render_template, request

app = Flask(__name__)

class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task, priority=None, deadline=None):
        new_task = {"task": task, "priority": priority, "deadline": deadline}
        self.tasks.append(new_task)

    def remove_task(self, index):
        try:
            del self.tasks[index]
            return "Task removed successfully."
        except IndexError:
            return "Invalid task index."

    def display_tasks(self):
        if self.tasks:
            tasks = [f"{i+1}. {task['task']} - Priority: {task['priority']}, Deadline: {task['deadline']}" 
                     for i, task in enumerate(self.tasks)]
            return "\n".join(tasks)
        else:
            return "No tasks."

    def mark_task_complete(self, index):
        try:
            del self.tasks[index]
            return "Task marked as complete."
        except IndexError:
            return "Invalid task index."

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            json.dump(self.tasks, file)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            return "File not found."

    def search_task(self, keyword):
        found_tasks = []
        for task in self.tasks:
            if keyword.lower() in task["task"].lower():
                found_tasks.append(task)
        if found_tasks:
            tasks = [f"{i+1}. {task['task']} - Priority: {task['priority']}, Deadline: {task['deadline']}" 
                     for i, task in enumerate(found_tasks)]
            return "\n".join(tasks)
        else:
            return "No matching tasks found."

todo_list = TodoList()
todo_list.load_from_file("tasks.json")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form.get("task")
    priority = request.form.get("priority")
    deadline = request.form.get("deadline")
    todo_list.add_task(task, priority, deadline)
    todo_list.save_to_file("tasks.json")
    return todo_list.display_tasks()

@app.route("/remove_task", methods=["POST"])
def remove_task():
    index = int(request.form.get("index")) - 1
    result = todo_list.remove_task(index)
    todo_list.save_to_file("tasks.json")
    return result

@app.route("/search_task", methods=["POST"])
def search_task():
    keyword = request.form.get("keyword")
    return todo_list.search_task(keyword)

@app.route("/mark_task_complete", methods=["POST"])
def mark_task_complete():
    index = int(request.form.get("index")) - 1
    result = todo_list.mark_task_complete(index)
    todo_list.save_to_file("tasks.json")
    return result

if __name__ == "__main__":
    app.run(debug=True)
