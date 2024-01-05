from pdg_app import create_app, db  # Importez l'application Flask et la base de données

# Créez une instance de l'application Flask
app = create_app()

# Utilisez l'application contexte pour accéder aux fonctionnalités de Flask-SQLAlchemy
with app.app_context():
    # Importez vos modèles SQLAlchemy
    from pdg_app.models import Doctor, PlanningMedecin, Preference

    # Initialisez l'inspecteur de la base de données
    inspector = db.inspect(db.engine)

    # Obtenez les noms des tables dans la base de données
    tables = inspector.get_table_names()
    print("Tables dans la base de données :", tables)

    # Pour effectuer une requête pour récupérer des données
    doctors = Doctor.query.all()
    for doctor in doctors:
        print(doctor.first_name, doctor.last_name)
    plannings = PlanningMedecin.query.all()
    for planning in plannings:
        print(planning.jour, planning.medecin)
    preferences = Preference.query.all()
    for pref in preferences:
        print(pref.day, pref.preference_garde,pref.preference_astreinte)
   

