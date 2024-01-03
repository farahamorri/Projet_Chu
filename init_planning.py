
"""
from pdg_app import db, create_app
from pdg_app.models import Doctor, Planning

planning = [9, 8, 1, 4, 6, 5, 7, 12, 3, 2, 3, 1, 5, 9, 7, 3, 9, 4, 2, 6, 9, 3, 12, 2, 5, 8, 10, 12, 11, 2]    

# Créez l'application Flask
app = create_app()

# Utilisez l'application contextuelle
with app.app_context():
    Session = db.sessionmaker(bind=db.engine)
    session = Session()

    for jour, id_medecin in enumerate(planning, start=1):
        record = Planning(jour=jour, id_medecin=id_medecin)
        session.add(record)
    session.commit()

result = (
    session.query(Planning.jour, Doctor.first_name, Doctor.last_name)
    .join(Doctor, Planning.id_medecin == Doctor.id)
    .all()
)
# Affichez les résultats
for jour, first_name, last_name in result:
    print(f"Jour: {jour}, Nom: {last_name}, Prénom: {first_name}")

    # Fermez la session
    session.close()





from pdg_app import db, create_app
from pdg_app.models import Doctor, Planning
from datetime import datetime, timedelta

planning =  [[9, 8, 1], [1, 4, 3]]

# Créez l'application Flask
app = create_app()

def calculer_identifiant(date, type_service):
    semestre = 1 if date.month <= 6 else 2
    if type_service == 'garde':
        type_abrege = 'g'
    else:
        type_abrege = 'a'
    return f"{semestre}-{date.year}-{date.day}-{type_abrege}"



def obtenir_info_medecin(identifiant):
    if identifiant in Doctor:
        medecin = Doctor[identifiant]
        return identifiant, medecin.first_name , medecin.last_name
    else:
        return None, None, None

# Reste du code inchangé jusqu'à transformer_liste

def transformer_liste(a, date):
    b = []
    for i, sous_liste in enumerate(a):
        for j, identifiant_medecin in enumerate(sous_liste):
            type_service = 'garde' if i == 0 else 'astreinte'
            identifiant = calculer_identifiant(date + timedelta(days=j), type_service)
            date_formattee = (date + timedelta(days=j)).strftime("%d/%m/%Y")
            id_medecin, prenom, nom = obtenir_info_medecin(identifiant_medecin)
            if id_medecin is not None:
                b.append([identifiant, date_formattee, id_medecin, prenom, nom, type_service])
    return b


# La date datetime
date_datetime = datetime.strptime("01/01/2023", "%d/%m/%Y")

# Transformation de la liste a en liste b selon les spécifications données
b = transformer_liste(a, date_datetime)

# Affichage de la liste b
print(b)

"""

from pdg_app import db, create_app
from pdg_app.models import Doctor, PlanningMedecin
from datetime import datetime, timedelta

# Ta fonction de calcul d'identifiant
def calculer_identifiant(date, type_service):
    semestre = 1 if date.month <= 6 else 2
    if type_service == 'garde':
        type_abrege = 'g'
    else:
        type_abrege = 'a'
    return f"{semestre}-{date.year}-{date.day}-{type_abrege}"

# Ta fonction pour obtenir les infos du médecin
def obtenir_info_medecin(identifiant):
    medecin = Doctor.query.filter_by(id=identifiant).first()
    if medecin:
        return medecin.id, medecin.first_name, medecin.last_name
    else:
        return None, None, None


# Ta fonction pour transformer la liste
def transformer_liste(a, date):
    b = []
    for i, sous_liste in enumerate(a):
        for j, identifiant_medecin in enumerate(sous_liste):
            type_service = 'garde' if i == 0 else 'astreinte'
            identifiant = calculer_identifiant(date + timedelta(days=j), type_service)
            date_formattee = (date + timedelta(days=j)).strftime("%d/%m/%Y")
            id_medecin, prenom, nom = obtenir_info_medecin(identifiant_medecin)
            if id_medecin is not None:
                b.append([identifiant, date_formattee, id_medecin, prenom, nom, type_service])
    return b

# Exemple de liste planning
planning =  [[9, 8, 1], [1, 4, 3]]

# Créer l'application Flask
app = create_app()

# Utiliser l'application contextuelle
with app.app_context():
    Session = db.sessionmaker(bind=db.engine)
    session = Session()

    # Transforme la liste selon tes spécifications
    date_datetime = datetime.strptime("01/01/2023", "%d/%m/%Y")
    b = transformer_liste(planning, date_datetime)

    # Affiche la liste b
    print(b)

    for item in b:
        identifiant, date_formattee, id_medecin, prenom, nom, type_service = item
        record = PlanningMedecin(jour=identifiant, id_medecin=id_medecin)
        session.add(record)    

    session.commit()
    # Ferme la session
    session.close()
