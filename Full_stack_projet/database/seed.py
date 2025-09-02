import os
from datetime import date, time, datetime
from flask import Flask
from models.mon_model import db, Patient, Doctor, Appointment

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/hopital_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def seed_data():
    with app.app_context():
        print("Initialisation de la base de données...")
        db.drop_all()
        db.create_all()

        print("Création des patients...")
        patients_data = [
            {'first_name': 'Jean', 'last_name': 'Dupont', 'date_of_birth': date(1985, 5, 12), 'contact_number': '0612345678', 'address': '1 rue de la Paix, Paris'},
            {'first_name': 'Marie', 'last_name': 'Durand', 'date_of_birth': date(1992, 10, 25), 'contact_number': '0623456789', 'address': '2 avenue des Champs, Paris'},
            {'first_name': 'Pierre', 'last_name': 'Lefebvre', 'date_of_birth': date(1978, 2, 18), 'contact_number': '0712345678', 'address': '3 boulevard Saint-Germain, Paris'},
            {'first_name': 'Sophie', 'last_name': 'Moreau', 'date_of_birth': date(1995, 7, 1), 'contact_number': '0723456789', 'address': '4 rue de Rivoli, Paris'},
            {'first_name': 'Luc', 'last_name': 'Petit', 'date_of_birth': date(1965, 11, 20), 'contact_number': '0812345678', 'address': '5 rue de la Liberté, Lyon'},
            {'first_name': 'Isabelle', 'last_name': 'Roux', 'date_of_birth': date(1988, 4, 30), 'contact_number': '0823456789', 'address': '6 place des Terreaux, Lyon'},
            {'first_name': 'Thomas', 'last_name': 'Leroy', 'date_of_birth': date(2001, 9, 15), 'contact_number': '0912345678', 'address': '7 rue de la Bourse, Marseille'},
            {'first_name': 'Camille', 'last_name': 'Girard', 'date_of_birth': date(1975, 3, 8), 'contact_number': '0923456789', 'address': '8 vieux port, Marseille'},
            {'first_name': 'Paul', 'last_name': 'Dubois', 'date_of_birth': date(1999, 6, 22), 'contact_number': '0634567890', 'address': '9 rue de l\'Hôtel de Ville, Toulouse'},
            {'first_name': 'Juliette', 'last_name': 'Martin', 'date_of_birth': date(1982, 12, 5), 'contact_number': '0645678901', 'address': '10 place du Capitole, Toulouse'}
        ]
        db.session.bulk_insert_mappings(Patient, patients_data)
        db.session.commit()

        print("Création des docteurs...")
        doctors_data = [
            {'first_name': 'Antoine', 'last_name': 'Bernard', 'specialization': 'Cardiologie', 'contact_number': '0655551111', 'email': 'a.bernard@hopital.com'},
            {'first_name': 'Laura', 'last_name': 'Dubois', 'specialization': 'Pédiatrie', 'contact_number': '0655552222', 'email': 'l.dubois@hopital.com'},
            {'first_name': 'Marc', 'last_name': 'Laurent', 'specialization': 'Généraliste', 'contact_number': '0655553333', 'email': 'm.laurent@hopital.com'},
            {'first_name': 'Elodie', 'last_name': 'Dupont', 'specialization': 'Dermatologie', 'contact_number': '0655554444', 'email': 'e.dupont@hopital.com'},
            {'first_name': 'Nicolas', 'last_name': 'Petit', 'specialization': 'Chirurgie', 'contact_number': '0655555555', 'email': 'n.petit@hopital.com'},
            {'first_name': 'Justine', 'last_name': 'Lemoine', 'specialization': 'Orthopédie', 'contact_number': '0655556666', 'email': 'j.lemoine@hopital.com'},
            {'first_name': 'François', 'last_name': 'Morel', 'specialization': 'Neurologie', 'contact_number': '0655557777', 'email': 'f.morel@hopital.com'},
            {'first_name': 'Manon', 'last_name': 'Lefevre', 'specialization': 'Ophtalmologie', 'contact_number': '0655558888', 'email': 'm.lefevre@hopital.com'},
            {'first_name': 'Julien', 'last_name': 'Garcia', 'specialization': 'Gynécologie', 'contact_number': '0655559999', 'email': 'j.garcia@hopital.com'},
            {'first_name': 'Charlotte', 'last_name': 'Rousseau', 'specialization': 'Endocrinologie', 'contact_number': '0655550000', 'email': 'c.rousseau@hopital.com'}
        ]
        db.session.bulk_insert_mappings(Doctor, doctors_data)
        db.session.commit()

        print("Création des rendez-vous...")
        appointments_data = [
            {'patient_id': 1, 'doctor_id': 3, 'appointment_date': date(2025, 8, 29), 'appointment_time': time(10, 0), 'reason': 'Contrôle annuel'},
            {'patient_id': 2, 'doctor_id': 2, 'appointment_date': date(2025, 8, 30), 'appointment_time': time(14, 30), 'reason': 'Vaccination'},
            {'patient_id': 3, 'doctor_id': 1, 'appointment_date': date(2025, 9, 1), 'appointment_time': time(9, 0), 'reason': 'Douleurs thoraciques'},
            {'patient_id': 4, 'doctor_id': 4, 'appointment_date': date(2025, 9, 2), 'appointment_time': time(11, 15), 'reason': 'Consultation pour éruption cutanée'},
            {'patient_id': 5, 'doctor_id': 7, 'appointment_date': date(2025, 9, 3), 'appointment_time': time(16, 0), 'reason': 'Maux de tête chroniques'},
            {'patient_id': 6, 'doctor_id': 6, 'appointment_date': date(2025, 9, 4), 'appointment_time': time(8, 30), 'reason': 'Suivi post-opératoire'},
            {'patient_id': 7, 'doctor_id': 8, 'appointment_date': date(2025, 9, 5), 'appointment_time': time(10, 30), 'reason': 'Examen de la vue'},
            {'patient_id': 8, 'doctor_id': 9, 'appointment_date': date(2025, 9, 6), 'appointment_time': time(15, 0), 'reason': 'Consultation de grossesse'},
            {'patient_id': 9, 'doctor_id': 10, 'appointment_date': date(2025, 9, 7), 'appointment_time': time(11, 0), 'reason': 'Bilan hormonal'},
            {'patient_id': 10, 'doctor_id': 5, 'appointment_date': date(2025, 9, 8), 'appointment_time': time(14, 0), 'reason': 'Chirurgie mineure'}
        ]
        db.session.bulk_insert_mappings(Appointment, appointments_data)
        db.session.commit()
        print("Seeding terminé avec succès!")

if __name__ == '__main__':
    app = create_app()
    seed_data()