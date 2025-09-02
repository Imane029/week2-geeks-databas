import os
from flask import Flask
from models.mon_model import db, User

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/hopital_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def create_initial_user():
    with app.app_context():
        # Crée la table `users` si elle n'existe pas
        db.create_all()
        
        # Vérifie si l'utilisateur existe déjà
        if not User.query.filter_by(username='admin').first():
            print("Création de l'utilisateur 'admin'...")
            user = User(username='admin')
            user.set_password('1234')  
            db.session.add(user)
            db.session.commit()
            print("Utilisateur 'admin' créé avec succès !")
        else:
            print("L'utilisateur 'admin' existe déjà.")

if __name__ == '__main__':
    app = create_app()
    create_initial_user()