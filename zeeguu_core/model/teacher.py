from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from zeeguu_core.model import User
from zeeguu_core.model.teacher_cohort_map import TeacherCohortMap
from zeeguu_core.server import db


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship(User)

    def __init__(self, user):
        self.user = user

    def get_cohorts(self):
        return TeacherCohortMap.get_cohorts_for(self.user)

    @classmethod
    def from_user(cls, user):
        cohort_count_of_user = len(TeacherCohortMap.get_cohorts_for(user))
        if cohort_count_of_user > 0:
            return cls(user)
        else:
            return None
