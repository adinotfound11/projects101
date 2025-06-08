from flask import Flask, request, redirect, send_from_directory, render_template_string, jsonify
import os, uuid, json, datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory DB
TASKS = []
REVISION_HISTORY = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>Game Dev Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #121212;
            color: #f0f0f0;
            margin: 0;
            padding: 0;
        }
        header {
            background: #1f1f1f;
            padding: 1rem;
            text-align: center;
            font-size: 1.8rem;
        }
        .container {
            padding: 2rem;
        }
        .task {
            background: #1e1e1e;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 10px;
        }
        .task input, .task textarea, .task select {
            width: 100%;
            margin-top: 0.5rem;
            padding: 0.5rem;
            border-radius: 5px;
        }
        .task button {
            margin-top: 0.5rem;
            padding: 0.5rem 1rem;
            background: #61dafb;
            border: none;
            cursor: pointer;
        }
        .dark-toggle {
            float: right;
            margin-right: 2rem;
        }
        .progress {
            width: 100%;
        }
        .subtasks {
            margin-top: 0.5rem;
        }
        .markdown {
            white-space: pre-wrap;
            background: #222;
            padding: 0.5rem;
            border-radius: 8px;
            margin-top: 1rem;
        }
    </style>
</head>
<body>
<header>
    Game Dev Tracker
    <button class=\"dark-toggle\" onclick=\"toggleTheme()\">Toggle Dark/Light</button>
</header>
<div class=\"container\">
    <form method=\"POST\" enctype=\"multipart/form-data\">
        <h2>New Task</h2>
        <input name=\"title\" placeholder=\"Task Title\" required>
        <textarea name=\"description\" placeholder=\"Description (Markdown supported)\"></textarea>
        <input type=\"date\" name=\"due_date\">
        <select name=\"priority\">
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
            <option>Critical</option>
        </select>
        <input type=\"text\" name=\"tags\" placeholder=\"Tags (comma-separated)\">
        <input type=\"text\" name=\"notes\" placeholder=\"Level Design Notes / Feature Roadmap\">
        <label>Progress:</label>
        <input type=\"range\" name=\"progress\" min=\"0\" max=\"100\" class=\"progress\">
        <input type=\"text\" name=\"subtasks\" placeholder=\"Subtasks (comma-separated)\">
        <input type=\"file\" name=\"attachment\">
        <button type=\"submit\">Add Task</button>
    </form>
    <hr>
    <input id=\"search\" placeholder=\"Search tasks...\" onkeyup=\"filterTasks()\">
    <div id=\"task-list\">
        {% for task in tasks %}
        <div class=\"task\">
            <strong contenteditable=\"true\">{{ task['title'] }}</strong> - <em>{{ task['priority'] }}</em><br>
            Due: {{ task['due_date'] }} | Progress: {{ task['progress'] }}%<br>
            <div class=\"markdown\">{{ task['description'] }}</div>
            Tags: {{ task['tags'] }}<br>
            Notes: {{ task['notes'] }}<br>
            Subtasks: <ul class=\"subtasks\">{% for sub in task['subtasks'] %}<li>{{ sub }}</li>{% endfor %}</ul>
            {% if task['filename'] %}
                <a href=\"/uploads/{{ task['filename'] }}\">Download Attachment</a><br>
            {% endif %}
            <form method=\"POST\" action=\"/delete/{{ task['id'] }}\">
                <button>Delete</button>
            </form>
            <details>
              <summary>Revision History</summary>
              <ul>
                {% for revision in history.get(task['id'], []) %}
                  <li>{{ revision }}</li>
                {% endfor %}
              </ul>
            </details>
        </div>
        {% endfor %}
    </div>
</div>
<script>
    function toggleTheme() {
        document.body.classList.toggle('light');
    }
    function filterTasks() {
        const query = document.getElementById('search').value.toLowerCase();
        const tasks = document.querySelectorAll('.task');
        tasks.forEach(task => {
            task.style.display = task.innerText.toLowerCase().includes(query) ? '' : 'none';
        });
    }
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("attachment")
        filename = ""
        if file and file.filename:
            filename = str(uuid.uuid4()) + "_" + file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        task_id = str(uuid.uuid4())
        description = request.form.get("description")
        task = {
            "id": task_id,
            "title": request.form.get("title"),
            "description": description,
            "due_date": request.form.get("due_date"),
            "priority": request.form.get("priority"),
            "tags": request.form.get("tags"),
            "notes": request.form.get("notes"),
            "progress": request.form.get("progress", "0"),
            "subtasks": [s.strip() for s in request.form.get("subtasks", "").split(",") if s.strip()],
            "filename": filename
        }
        TASKS.append(task)
        REVISION_HISTORY[task_id] = [f"Initial: {description[:50]}..."]
        return redirect("/")
    return render_template_string(HTML_TEMPLATE, tasks=TASKS, history=REVISION_HISTORY)

@app.route("/delete/<id>", methods=["POST"])
def delete_task(id):
    global TASKS
    TASKS = [t for t in TASKS if t['id'] != id]
    REVISION_HISTORY.pop(id, None)
    return redirect("/")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
