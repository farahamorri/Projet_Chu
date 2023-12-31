from flask import Flask, jsonify
import numpy as np
import copy
from datetime import datetime, date, timedelta
from flask_sqlalchemy import SQLAlchemy
#from pdg_app.models import Preference
from pdg_app.models import Doctor

from pdg_app import create_app, db # Importez l'application Flask et la base de données

# Créez une instance de l'application Flask
app = create_app()

# Utilisez l'application contexte pour accéder aux fonctionnalités de Flask-SQLAlchemy
with app.app_context():
    Session = db.sessionmaker(bind=db.engine)
    session = Session()
    # Importez vos modèles SQLAlchemy
    from pdg_app.models import Preference

    # Initialisez l'inspecteur de la base de données
    inspector = db.inspect(db.engine)

    # Pour effectuer une requête pour récupérer des données
    preferences = Preference.query.all()
    sorted_preferences = sorted(preferences, key=lambda pref: (pref.department, pref.day, pref.id_medecin))
    L = []
    for preference in sorted_preferences:
        preference_info = [preference.department, preference.day, preference.id_medecin, preference.preference_garde, preference.preference_astreinte]
        L.append(preference_info)

    # Pour récupérer la liste Service associée aux médecins (L_department)
    doctors = session.query(Doctor).all()
    sorted_doctors = sorted(doctors, key=lambda doc: (doc.department, doc.id))

    L_department= []
    current_department = None
    current_department_doctors = []

    for doctor in sorted_doctors:
        if current_department is None or doctor.department != current_department:
            # Nouveau département, ajouter la liste des médecins actuels à la liste principale
            if current_department_doctors:
                L_department.append(current_department_doctors)
            # Réinitialiser la liste pour le nouveau département
            current_department_doctors = [doctor]
            current_department = doctor.department
        else:
            # Même département, ajouter le médecin à la liste actuelle
            current_department_doctors.append(doctor)

    # Ajouter la dernière liste de médecins à la liste principale
    if current_department_doctors:
        L.append(current_department_doctors)


db = SQLAlchemy(app)

#association jour/nombre 

date = date(2023, 11, 1)
L_jour = [date]
for i in range(180):
    date = date + timedelta(days=1)
    L_jour.append(date)

for i in range(len(L)):
    for j in range(180):
        if L[i][1] == L_jour[j] : 
            L[i][1] = j
            
#pour avoir nJ :
  
L_jour = []
for i in range(len(L)):
    L_jour.append(L[i][1])
    
L_jour_sans_doublons = list(set(L_jour))
    
nombre_de_jours = 0    
for i in range(len(L_jour_sans_doublons)-1):
    if L_jour_sans_doublons[i+1] != L_jour_sans_doublons[i]:
        nombre_de_jours += 1


#association service/nombre + donne nS

nombre_de_services = 0
L_adapte = copy.deepcopy(L)
L_adapte[0][0]= nombre_de_services
for i in range(len(L_adapte)-1): 
    if L[i+1][0] != L[i][0]:
        nombre_de_services +=1
        L_adapte[i+1][0]= nombre_de_services
    else : 
        L_adapte[i+1][0]= nombre_de_services
        
print(L_adapte)


nombre_medecins = L_adapte[-1][2]
    
def générer_planning_garde(Liste_adapte): 
    L = np.full((nombre_de_services+1,nombre_de_jours+1,nombre_medecins), 1)
    for i in range(len(Liste_adapte)):
        s = Liste_adapte[i][0]
        j = Liste_adapte[i][1]
        m = Liste_adapte[i][2] -1
        L[s][j][m] = Liste_adapte[i][3]
    return L
                    
A = générer_planning_garde(L_adapte)

def générer_planning_astreinte(Liste_adapte): 
    L = np.full((nombre_de_services+1,nombre_de_jours+1,nombre_medecins), 1)
    for i in range(len(Liste_adapte)):
        s = Liste_adapte[i][0]
        j = Liste_adapte[i][1]
        m = Liste_adapte[i][2] - 1
        L[s][j][m] = Liste_adapte[i][4]
    return L

B = générer_planning_astreinte(L_adapte)


def générer_planning(L1,L2):
    L = []
    for i in range(len(L1)):
        L.append(L1[i])
        L.append(L2[i])
    return L

L_finale = générer_planning(A,B)
print(L_finale)