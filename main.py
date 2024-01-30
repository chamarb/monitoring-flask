from controller import app
import os
from dal import Database
from models import db

def initialize_database():
    script_path = 'db/init.sql'
    Database.execute_script(script_path)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initialize_database()

    port:int=int(os.environ.get('PORT',8080))
    app.run(debug=True,host='0.0.0.0',port=8080)