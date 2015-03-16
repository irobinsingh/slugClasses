# -*- coding: utf-8 -*-
from datetime import datetime


db.define_table('professor',
                Field('first_name', required=True),
                Field('last_name', required=True)
                )

db.define_table('subject',
                Field('acronym', unique=True),
                Field('title'))

db.define_table('course',
                Field('subject', db.subject),
                Field('nbr', label="number"),
                Field('title'),
                )

db.define_table('revision',
                Field('course_id', db.course),
                Field('professor_id', db.professor),
                Field('author'),
                Field('date_created', 'datetime',default=datetime.utcnow()),
                Field('summary'),
                Field('body', 'text'),
                )

db.course.subject.requires = IS_IN_DB(db, 'subject.id', '%(acronym)s: %(title)s')
db.revision.professor_id.requires = IS_IN_DB(db, 'professor.id', '%(last_name)s, %(first_name)s')
db.revision.date_created.writable=False
db.revision.date_created.readable=False