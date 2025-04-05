from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class EncryptedData(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    original_text=db.Column(db.Text,nullable=False)
    encrypted_text=db.Column(db.Text,nullable=False)
