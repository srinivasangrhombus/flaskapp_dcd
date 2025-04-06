from flask import request,jsonify,Blueprint

from  cryptography.fernet import Fernet

from models.encrypted import db,EncryptedData

import os

#define a blueprint for modular routes 
encryption_bp=Blueprint("encryption", __name__ )


#load encrypted key form .env
key = os.getenv("ENCRYPTION_KEY")
cipher_suite=Fernet(key.encode())

#post method for ecrypt-and-store API Route creation

@encryption_bp.route("/encrypt-and-store",methods=["POST"])
def Encrypt_and_Store():
    data=request.json
    text=data.get("text","")

    if not text:
        return jsonify({"error":"no text provided in the request"}),400
    
    encrypted=cipher_suite.encrypt(text.encode()).decode()

    record=EncryptedData(original_text=text,encrypted_text=encrypted)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message:":"data encrypted and stored","id":record.id})


#fetch all record using get method 
@encryption_bp.route("/records",methods=["GET"])
def get_Records():
    records=EncryptedData.query.all()

    return jsonify([
        {
            "id":r.id,
            "original_text":r.original_text,
            "encrypted_text":r.encrypted_text
        }
        for r in records
    ])