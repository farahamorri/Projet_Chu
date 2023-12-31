# pdg_app/views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from pdg_app import db
from pdg_app.models import Doctor, Preference, Planning, DepartmentEnum, get_department_enum
from datetime import datetime

auth = Blueprint('auth', __name__)

# Page d'accueil du site web
@auth.route('/')
def home():
    return render_template('home.html')


# Page de conexion 
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        json_data = request.get_json()
        email = json_data['email']
        password = json_data['password']
        doctor = Doctor.query.filter_by(email=email).first()
        name=doctor.first_name+" "+doctor.last_name

        print('Email: ',email)
        print('Doctor: ', doctor)
        print('Pass: ',password)
        print('nom: ',name)

        if (not (doctor is None)) and (password == doctor.password):
            #login_user(doctor)
            #return redirect(url_for('auth.dashboard'))  # Rediriger vers la page du tableau de bord
            return jsonify({"success": True, "message": "Connexion réussie", "name": name, "email": email}), 200, {'Content-Type': 'application/json'}
        else:
            #flash('La connexion a échoué. Vérifiez votre adresse e-mail et votre mot de passe.', 'danger')
            return jsonify({"success": False, "message": "Connexion échouée. Vérifiez votre adresse e-mail et votre mot de passe."}), 200, {'Content-Type': 'application/json'}
    return render_template('login.html')


# Page d'inscription
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        department_str = request.form.get('department')

        try:
            department = get_department_enum(department_str)
        except ValueError as e:
            flash(f"Error: {e}", 'danger')
            return redirect(url_for('auth.register'))
        new_doctor = Doctor(first_name=first_name, last_name=last_name, email=email, password=password, department=department)
        db.session.add(new_doctor)
        db.session.commit()

        flash('Votre compte a été créé avec succès. Vous pouvez vous connecter maintenant.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# LogOut
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# Page tableau de bord (emplois du temps perso + du service)
@auth.route('/planning')
@login_required
def planning():
    # Affiche les emplois du temps personnels
    personal_shifts = Planning.query.filter_by(doctor_id=current_user.id).all()

    # Affiche l'emploi du temps général du service
    department_shifts = Planning.query.filter(Planning.department == current_user.department.value).all()

    return render_template('dashboard.html', personal_shifts=personal_shifts, department_shifts=department_shifts)


from flask import jsonify, abort

@auth.route('/preferences', methods=['POST'])
def preferences():
    if request.method == 'POST':
        data = request.get_json()
        date = data.get('date')
        dispo = data.get('dispo')
        garde = data.get('garde')
        astreinte = data.get('astreinte')
        email = data.get('email')

        print('Email: ',email)
        print('astreinte: ', astreinte)
        print('date: ',date)

        #parsed_date = datetime.fromisoformat(date)

        #date_str = '2023-12-14T23:00:00.000Z'
        date_str = date
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            # Utiliser parsed_date dans le reste de ton code Flask
        except ValueError as e:
            print(f"Erreur de conversion de la date : {e}")
            # Gérer l'erreur de conversion

        
        print('Email: ',email)
        print('astreinte: ', astreinte)
        print('date: ',parsed_date)

        if dispo == 100:
            return jsonify({"error": "Préférence invalide"}), 400  # Code d'erreur 400 pour une requête incorrecte

        elif not email:
            return jsonify({"error": "Connexion requise pour récupérer les données"}), 401  # Code d'erreur 401 pour une erreur d'authentification

        else:
            doctor = Doctor.query.filter_by(email=email).first()
            if doctor:
                new_preference = Preference(
                    doctor_id=doctor.id,
                    day=parsed_date,
                    preference_garde=dispo if garde else 1,
                    preference_astreinte=dispo if astreinte else 1
                )

                db.session.add(new_preference)
                db.session.commit()

                # all_preferences = Preference.query.filter_by(doctor_id=doctor.id).first()

                # # Convertir les préférences en une liste dictionnaires
                # preferences_list = []
                # for preference in all_preferences:
                #     preferences_list.append({
                #         'date': preference.day,
                #         'preference_garde': preference.preference_garde,
                #         'preference_astreinte': preference.preference_astreinte
                #     })

                # Renvoyer les préférences au format JSON
                return jsonify(preferences_list),jsonify({"success": True, "message": "Préférences enregistrées avec succès"}), 200  # Code de succès 200

            else:
                return jsonify({"error": "Médecin non trouvé"}), 404  # Code d'erreur 404 si le médecin n'est pas trouvé



@auth.route('/tableau', methods=['GET'])
def tableau():
    return render_template('tableau.html')

