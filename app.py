import os
from flask import Flask
from dotenv import load_dotenv
from models.encrypted import db #sqlalchemy instance and models
from routes.encryption import encryption_bp #API Routes



#load environmental variabeles form .env file 
load_dotenv()

#Initialize flask app

app =Flask(__name__)


#Configuring database using environmental variables

app.config['SQLALCHEMY_DATABASE_URI'] =(
    f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    
    )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


#Intialize SQLALCHEMY with app
db.init_app(app)

#create tables(only needed once or if Db is empty)
with app.app_context():
    db.create_all()

#Register blueprint for encryption Api Routes
app.register_blueprint(encryption_bp)

#run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
    


