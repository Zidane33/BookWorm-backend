from .model import Project
from app import db


def addProjectToDatabase(project, user):
    p = Project(title=project, user_id=user)
    db.session.add(p)
    db.session.commit()
