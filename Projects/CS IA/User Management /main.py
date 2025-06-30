from flask import Flask, request, jsonify, render_template_string
import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")  # Ensure the JSON is in the same directory
firebase_admin.initialize_app(cred)
db = firestore.client()

# Embedded HTML + CSS + JS
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Create User</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #31363F;
      color: #EEE;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    form {
      background: #222831;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 0 12px rgba(0,0,0,0.4);
    }
    input, select, button {
      display: block;
      margin: 15px 0;
      padding: 10px;
      width: 100%;
    }
    button {
      background: #76ABAE;
      color: #000;
      font-weight: bold;
      border: none;
      cursor: pointer;
    }
    .message {
      margin-top: 10px;
      font-size: 0.9rem;
    }
  </style>
</head>
<body>
  <form id="createForm">
    <h2>Create New User</h2>
    <input type="text" id="name" placeholder="Name" required />
    <input type="email" id="email" placeholder="Email" required />
    <select id="role">
      <option value="student">Student</option>
      <option value="counselor">Counselor</option>
      <option value="coordinator">Coordinator</option>
    </select>
    <button type="submit">Create User</button>
    <div class="message" id="msg"></div>
  </form>

  <script>
    document.getElementById("createForm").addEventListener("submit", async function(e) {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const email = document.getElementById("email").value;
      const role = document.getElementById("role").value;
      const msg = document.getElementById("msg");

      const res = await fetch("/create_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, role })
      });

      const data = await res.json();
      msg.textContent = data.success ? "User created successfully!" : "Error: " + data.error;
      msg.style.color = data.success ? "lightgreen" : "salmon";
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name", "")
    email = data.get("email")
    role = data.get("role")

    if not email or not role:
        return jsonify({"success": False, "error": "Missing email or role"}), 400

    try:
        user = auth.create_user(email=email, password="12345678")
        auth.set_custom_user_claims(user.uid, {"role": role})
        db.collection("users").document(user.uid).set({
            "name": name,
            "email": email,
            "role": role,
            "firstLogin": True
        })
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
