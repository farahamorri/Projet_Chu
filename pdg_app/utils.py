import mop

from pdg_app.models import Content, Gender

def find_content(gender):
    contents = Content.query.filter(Content.gender == Gender[gender]).all()
    return random.choice(contents)