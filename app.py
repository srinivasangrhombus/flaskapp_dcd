import os

from flask import Flask,request,jsonify
from cryptography.fernet import Fernet
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get the encryption key from .env
key = os.getenv("ENCRYPTION_KEY")

if not key or key.strip() == "":  # If key is missing or empty, generate a new one
    key = Fernet.generate_key().decode()  

    # Read existing .env content if available
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            lines = f.readlines()

        # Remove old ENCRYPTION_KEY entries
        new_lines = [line for line in lines if not line.startswith("ENCRYPTION_KEY=")]

        # Write the new .env file with the generated key
        with open(".env", "w") as f:
            f.writelines(new_lines)
            f.write(f"ENCRYPTION_KEY={key}\n")

    print("Generated new ENCRYPTION_KEY and saved to .env")
else:
    print(f"Using existing ENCRYPTION_KEY: {key}")

# ✅ Initialize `cipher_suite` after the key is set
cipher_suite = Fernet(key.encode())
@app.route("/encrypt",methods=["Post"])
def encrypteData():
    data=request.json
    text=data.get("text","")

    if not text:
        return jsonify({"error":"no text found in request"}),400
    

    encryptedData=cipher_suite.encrypt(text.encode()).decode()

    return jsonify({"encryptedData":encryptedData})

@app.route("/decrypt",methods=["post"])
def decryptedData():
    data =request.json
    text= data.get("text","")

    if not text:
        return jsonify({"error":"no text found in request for decrypting"}),400
    
    decryptedData=cipher_suite.decrypt(text.encode()).decode()

    return jsonify({"decryptedData":decryptedData})




# Database configuration from environment variable

app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL","postgresql://postgres:fap123@localhost:5432/mydatabase")

if __name__== "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)