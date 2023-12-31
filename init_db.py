# init_db.py
from pdg_app import db, create_app
from pdg_app.models import Doctor
from pdg_app.models import Preference
from pdg_app.models import Planning
import logging as lg
from datetime import datetime, timedelta

planning = [9, 8, 1, 4, 6, 5, 7, 12, 3, 2, 3, 1, 5, 9, 7, 3, 9, 4, 2, 6, 9, 3, 12, 2, 5, 8, 10, 12, 11, 2] 

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(Doctor("Myriam", "Moussa", "myriam@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Thomas", "Tremoureux", "thomas@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Maxime", "Edouard", "maxime@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Bastien", "Pereira", "bastien@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Jeanne", "Mithieux", "jeanne@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Ilan", "Saffarti", "ilan@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Julnar", "Nakoula", "julnar@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Simon", "Peugeot", "simon@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Nassim", "Azouzi", "nassim@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Alexandre", "Cymes", "alexandre@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Farah", "Amorri", "farah@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Lucile", "Picandet", "lucile@centrale.fr", "coucou", "urgences"))
    db.session.add(Doctor("Jean_Marie", "Renart", "jmr@centrale.fr", "coucou", "urgences"))

    db.session.commit()
    lg.warning('Database initialized!')
    

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








"""""
    db.session.add(Preference('2', "urgences", "2023-11-01", '0', '-1'))
    db.session.add(Preference('3', "urgences", "2023-11-01", '-1', '0'))
    db.session.add(Preference('1', "urgences", "2023-11-01", '-1', '-1')) 
    db.session.add(Preference('4', "urgences", "2023-11-01", '0', '0'))
    db.session.add(Preference('2', "urgences", "2023-11-02", '0', '0'))
    db.session.add(Preference('3', "urgences", "2023-11-02", '-1', '-1'))
    db.session.add(Preference('1', "urgences", "2023-11-02", '0', '0'))
    db.session.add(Preference('4', "urgences", "2023-11-02", '0', '-1'))
    db.session.add(Preference('5', "urgences", "2023-11-01", '0', '0'))
    db.session.add(Preference('6', "urgences", "2023-11-01", '-1', '-1'))
    db.session.add(Preference('7', "urgences", "2023-11-01", '0', '-1'))
    db.session.add(Preference('5', "urgences", "2023-11-02", '0', '0'))
    db.session.add(Preference('6', "urgences", "2023-11-02", '-1', '-1'))
    db.session.add(Preference('7', "urgences", "2023-11-02", '0', '-1'))

    db.session.commit()
    lg.warning('Database initialized!')

    #db.session.add(Preference())

    start_date = datetime(2023,1,1)
    for jour, id_medecin in enumerate(planning, start=1):
        date = start_date + timedelta(days = jour-1)
        record = PlanningMedecin(jour=jour, id_medecin=id_medecin)
        db.session.add(record)
    result = (
    db.session.query(PlanningMedecin.jour, Doctor.first_name, Doctor.last_name)
    .join(Doctor, PlanningMedecin.id_medecin == Doctor.id)
    .all()
    )
    for jour, first_name, last_name in result:
        print(f"Jour: {jour}, Nom: {last_name}, Prénom: {first_name}")
"""""

