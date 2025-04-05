from flask import Blueprint, request, jsonify
from cryptography.fernet import Fernet
from models.encrypted import db, EncryptedData
import os

# Define a Blueprint for modular routes
encryption_bp = Blueprint("encryption", __name__)

# Load encryption key
key = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(key.encode())

# POST /encrypt-and-store
@encryption_bp.route("/encrypt-and-store", methods=["POST"])
def encrypt_and_store():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    encrypted = cipher_suite.encrypt(text.encode()).decode()

    record = EncryptedData(original_text=text, encrypted_text=encrypted)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Data encrypted and stored", "id": record.id})

# GET /records
@encryption_bp.route("/records", methods=["GET"])
def get_records():
    records = EncryptedData.query.all()
    return jsonify([
        {"id": r.id, "original_text": r.original_text, "encrypted_text": r.encrypted_text}
        for r in records
    ])
