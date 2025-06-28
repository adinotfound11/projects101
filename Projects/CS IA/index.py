from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Campus Connect</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #0f172a;
      --bg-sidebar: #111827;
      --bg-card: #ffffff;
      --bg-highlight: #d1fae5;
      --bg-progress-bg: #e5e7eb;
      --bg-progress-bar: #134e4a;
      --text-muted: #94a3b8;
      --text-main: #111827;
      --accent: #134e4a;
      --button-bg: #134e4a;
      --button-text: #ffffff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', sans-serif;
      display: flex;
      height: 100vh;
      background-color: var(--bg-dark);
      color: var(--text-main);
    }

    .sidebar {
      width: 220px;
      background-color: var(--bg-sidebar);
      padding: 24px 16px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .sidebar h2 {
      color: white;
      font-size: 18px;
      font-weight: 600;
    }

    .nav-link {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 12px;
      border-radius: 8px;
      color: var(--text-muted);
      font-size: 15px;
      font-weight: 500;
      cursor: pointer;
    }

    .nav-link.active {
      background-color: var(--accent);
      color: white;
    }

    .main {
      flex: 1;
      padding: 24px;
      background-color: var(--bg-dark);
      display: flex;
      flex-direction: column;
    }

    .top-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
    }

    .top-bar h1 {
      color: white;
      font-size: 20px;
      font-weight: 600;
    }

    .logout-btn {
      background-color: #1f2937;
      color: white;
      padding: 6px 12px;
      border: none;
      border-radius: 6px;
      font-size: 14px;
      cursor: pointer;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(2, 120px) 60px;
      gap: 16px;
    }

    .card {
      background-color: var(--bg-card);
      color: var(--text-main);
      padding: 16px;
      border-radius: 12px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      font-size: 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .card h3 {
      font-size: 14px;
      font-weight: 600;
    }

    .card p {
      font-size: 32px;
      font-weight: 600;
      margin-top: 8px;
    }

    .card ul {
      margin-top: 10px;
      padding-left: 18px;
      font-size: 14px;
    }

    .highlight {
      background-color: var(--bg-highlight);
      justify-content: center;
      align-items: center;
    }

    .highlight button {
      background-color: var(--button-bg);
      color: var(--button-text);
      font-size: 15px;
      padding: 10px 20px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
    }

    .progress-container {
      flex-direction: column;
    }

    .progress-bar-wrapper {
      background-color: var(--bg-progress-bg);
      border-radius: 6px;
      height: 12px;
      overflow: hidden;
      margin-top: 12px;
    }

    .progress-bar {
      width: 40%;
      height: 100%;
      background-color: var(--bg-progress-bar);
    }
  </style>
</head>
<body>
  <div class="sidebar">
    <h2>Campus Connect</h2>
    <div class="nav-link active">Dashboard</div>
    <div class="nav-link">Students</div>
    <div class="nav-link">Applications</div>
    <div class="nav-link">Reports</div>
  </div>
  <div class="main">
    <div class="top-bar">
      <h1>Dashboard</h1>
      <button class="logout-btn">Log Out</button>
    </div>
    <div class="grid">
      <div class="card">
        <h3>Total Students</h3>
        <p>120</p>
      </div>
      <div class="card">
        <h3>Upcoming Deadlines</h3>
        <ul>
          <li>October 15th - Application A</li>
          <li>November 1 - Application B</li>
        </ul>
      </div>
      <div class="card highlight">
        <button>+ New Student</button>
      </div>
      <div class="card">
        <h3>Application Progress</h3>
      </div>
      <div class="card progress-container" style="grid-column: span 2;">
        <h3>Application Progress</h3>
        <div class="progress-bar-wrapper">
          <div class="progress-bar"></div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
    """)

if __name__ == '__main__':
    app.run(debug=True)
