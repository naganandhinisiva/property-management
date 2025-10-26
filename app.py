from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# 🔌 MySQL Database Configuration
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # 🔁 Replace with your actual MySQL username
        password="nandhu", # 🔁 Replace with your MySQL password
        database="property_db"          # ✅ Ensure this matches your database name
    )

# 🌐 Home Page
@app.route("/")
def index():
    return render_template("index.html")

# 📄 Get All Properties
@app.route("/properties", methods=["GET"])
def get_properties():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

# ➕ Add a New Property
@app.route("/add", methods=["POST"])
def add_property():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO properties (address, owner, price, status) VALUES (%s, %s, %s, %s)",
                   (data['address'], data['owner'], data['price'], data['status']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# ❌ Delete Property by ID
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_property(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM properties WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

# 🚀 Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
