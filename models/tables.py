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
                Field('date_created', 'datetime', writable=False, default=datetime.utcnow()),
                Field('body', 'text'),
                Field('thumbsups', 'integer', readable=False),
                Field('thumbsdowns', 'integer', readable=False)
                )

db.define_table('note',
                Field('course_id', db.course),
                Field('date_created', 'datetime'),
                Field('body', 'text'),
                Field('thumbsups', 'integer', readable=False),
                Field('thumbsdowns', 'integer', readable=False)
                )

db.course.subject.requires = IS_IN_DB(db, 'subject.id', '%(acronym)s: %(title)s')
    