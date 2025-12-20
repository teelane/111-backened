from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# constant
DB_NAME = "budget_manager.db"


def init_db():
  conn = sqlite3.connect(DB_NAME) # opens a connection to the database file named "budget_manager.db"
  cursor = conn.cursor() # creates a cursor/tool that lets us send commands (SELECT, INSERT, ...)

  # ----- users table -----
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL             
  )
  """)

  conn.commit() # Save changes to the database
  conn.close() # Close de connection to the database


@app.get("/api/health")
def health_check():
  return jsonify({"status": "OK"}), 200


@app.post("/api/register")
def register():
  data = request.get_json()
  username = data.get("username")
  password = data.get("password")

  conn = sqlite3.connect(DB_NAME) # opens the connection to the db
  cursor = conn.cursor() # creates a cursor/tool (SELECT, INSERT)

  cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password)) # Executes the SQL statement
  conn.commit() # Save changes to the database
  conn.close() # Close de connection to the database

  return jsonify({
    "success": True,
    "message": "User registered successfully"  
  }), 201


@app.post("/api/login")
def login():
  data = request.get_json()
  username = data.get("username")
  password = data.get("password")

  conn = sqlite3.connect(DB_NAME)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
  user = cursor.fetchone()
  conn.close()

  if user and user["password"] == password:
    return jsonify({
      "user_id": user["id"], 
      "username": user["username"]
    }), 200
  
  return jsonify({
    "success": False,
    "message": "Invalid credentials"
  }), 401 # Unauthorized


@app.get("/api/users/<int:user_id>")
def get_user_by_id(user_id):
  conn = sqlite3.connect(DB_NAME)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
  user = cursor.fetchone()
  conn.close()

  if user:
    return jsonify({
      "id": user["id"],
      "username": user["username"]
    })
  
  return jsonify({
    "success": False,
    "message": "User not found"
  }), 404


if __name__ == "__main__":
  init_db()
  app.run(debug=True)

