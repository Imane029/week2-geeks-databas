import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models.mon_model import db, Patient, Doctor, Appointment, User
from sqlalchemy import func
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/hopital_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2d08ca45f6c9ea2da3bc2f93fd9ccc6460837486aa8'


db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# =================================================================
# ROUTES D'AUTHENTIFICATION
# =================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('login'))

# =================================================================
# ROUTE DE LA PAGE D'ACCUEIL 
# =================================================================
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# =================================================================
# ROUTES DES PATIENTS (CRUD et Recherche)
# =================================================================
@app.route('/patients')
@login_required
def list_patients():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search')
    if search_query:
        patients = Patient.query.filter(
            (Patient.first_name.ilike(f'%{search_query}%')) | 
            (Patient.last_name.ilike(f'%{search_query}%'))
        ).paginate(page=page, per_page=6)
    else:
        patients = Patient.query.paginate(page=page, per_page=6)
    return render_template('patients/list.html', patients=patients, search_query=search_query)

@app.route('/patients/create', methods=['GET', 'POST'])
@login_required
def create_patient():
    if request.method == 'POST':
        try:
            date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            new_patient = Patient(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                date_of_birth=date_of_birth,
                contact_number=request.form['contact_number'],
                address=request.form['address']
            )
            db.session.add(new_patient)
            db.session.commit()
            flash('Le patient a été ajouté avec succès !', 'success')
            return redirect(url_for('list_patients'))
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue : {e}', 'error')
    return render_template('patients/create.html')

@app.route('/patients/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        try:
            date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
            patient.first_name = request.form['first_name']
            patient.last_name = request.form['last_name']
            patient.date_of_birth = date_of_birth
            patient.contact_number = request.form['contact_number']
            patient.address = request.form['address']
            db.session.commit()
            flash('Les informations du patient ont été mises à jour.', 'success')
            return redirect(url_for('list_patients'))
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue : {e}', 'error')
    return render_template('patients/edit.html', patient=patient)

@app.route('/patients/delete/<int:id>', methods=['POST'])
@login_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    try:
        db.session.delete(patient)
        db.session.commit()
        flash('Le patient a été supprimé.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Une erreur est survenue lors de la suppression : {e}', 'error')
    return redirect(url_for('list_patients'))

@app.route('/patients/<int:id>')
@login_required
def details_patient(id):
    patient = Patient.query.get_or_404(id)
    appointments = Appointment.query.filter_by(patient_id=id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('patients/details.html', patient=patient, appointments=appointments)

# =================================================================
# ROUTES DES DOCTEURS
# =================================================================
@app.route('/doctors')
@login_required
def list_doctors():
    doctors = Doctor.query.all()
    return render_template('doctors/list.html', doctors=doctors)

@app.route('/doctors/<int:id>')
@login_required
def details_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    appointments = Appointment.query.filter_by(doctor_id=id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('doctors/details.html', doctor=doctor, appointments=appointments)

# =================================================================
# ROUTES DES RENDEZ-VOUS
# =================================================================
@app.route('/appointments')
@login_required
def list_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('appointments/list.html', appointments=appointments)

@app.route('/appointments/create', methods=['GET', 'POST'])
@login_required
def create_appointment():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    if request.method == 'POST':
        print("Données du formulaire:", request.form)
        try:
            appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
            appointment_time = datetime.strptime(request.form['appointment_time'], '%H:%M').time()
            reason = request.form['reason']
            
            
            patient_id_str = request.form.get('patient_id')
            doctor_id_str = request.form.get('doctor_id')

            if not patient_id_str or not doctor_id_str:
                flash('Veuillez sélectionner un patient et un médecin.', 'error')
                return redirect(url_for('create_appointment'))

           
            patient_id = int(patient_id_str)
            doctor_id = int(doctor_id_str)

            new_appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason
            )
            
            db.session.add(new_appointment)
            db.session.commit()
            
            flash('Le rendez-vous a été ajouté avec succès !', 'success')
            return redirect(url_for('list_appointments'))
        
        except ValueError:
            db.session.rollback()
            flash('Une erreur est survenue. Les données du formulaire ne sont pas valides.', 'error')
            return redirect(url_for('create_appointment'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Une erreur est survenue lors de la création du rendez-vous : {e}', 'error')
            return redirect(url_for('create_appointment'))
            
    return render_template('appointments/create.html', patients=patients, doctors=doctors)
# =================================================================
# ROUTES DES STATISTIQUES dial chartjs
# =================================================================
@app.route('/stats')
@login_required
def stats():
    patient_count = db.session.query(Patient).count()
    doctor_count = db.session.query(Doctor).count()
    appointment_count = db.session.query(Appointment).count()
    
    specialization_counts = db.session.query(Doctor.specialization, func.count(Appointment.doctor_id)).join(Appointment).group_by(Doctor.specialization).all()
    
    specializations = [row[0] for row in specialization_counts]
    counts = [row[1] for row in specialization_counts]
    
    return render_template('stats.html', 
                            patient_count=patient_count, 
                            doctor_count=doctor_count, 
                            appointment_count=appointment_count,
                            specializations=specializations,
                            counts=counts)

if __name__ == '__main__':
    app.run(debug=True)
