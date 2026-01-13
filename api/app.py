from flask import Flask, request
import hashlib
import subprocess
import os

app = Flask(__name__)

# Mot de passe en dur (mauvaise pratique)
#ADMIN_PASSWORD = "123456"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "") 


# Cryptographie faible (MD5)
def hash_password(password):
    
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")

    # Authentification faible
    if username == "admin" and hash_password(password) == hash_password(ADMIN_PASSWORD):
        return "Logged in"

    return "Invalid credentials"

@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")

    # Injection de commande (shell=True)
    result = subprocess.check_output(
         ["ping", "-c", "1", host],
        stderr=subprocess.STDOUT,
        text=True
    )
        
    
    return result

@app.route("/hello")
def hello():
    name = request.args.get("name", "user")

    # XSS potentiel
    #return f"<h1>Hello {name}</h1>"
    return f"Hello {name}"


if __name__ == "__main__":
    # Debug activé
    #app.run(debug=True)
    app.run(debug=False)
