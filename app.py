import os
import psycopg2

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

# ✅ Initialize cipher_suite after the key is set
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



# Database configuration using environment variables
db_user = os.getenv('DATABASE_USER', 'postgres')
db_password = os.getenv('DATABASE_PASSWORD', 'fap123')
db_host = os.getenv('DATABASE_HOST', 'localhost')
db_port = os.getenv('DATABASE_PORT', '5432')
db_name = os.getenv('DATABASE_NAME', 'mydatabase')


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy DB instance

@app.route("/db-check")
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT'),
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD')
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        conn.close()
        return jsonify({"status": "success", "postgres_version": version})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})







if __name__== "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
