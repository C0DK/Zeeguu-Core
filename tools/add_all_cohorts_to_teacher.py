#!/usr/bin/env python

"""

   Script that lists recent users

   To be called from a cron job.

"""
from zeeguu_core.server import db
from zeeguu_core.model import User, Cohort, TeacherCohortMap

if __name__ == "__main__":
    session = db.session
    big_teacher = User.query.filter_by(id=534).one()

    for cohort in Cohort.query.all():
        mapping = TeacherCohortMap.find_or_create(big_teacher, cohort, session)
        session.add(mapping)

    session.commit()
