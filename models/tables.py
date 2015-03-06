# -*- coding: utf-8 -*-
from datetime import datetime

CATEGORY = ['ACEN', 'AMS', 'ANTH', 'ART', 'BIO', 'CHEM', 'CMPE',
             'CMPS', 'ECON'],


db.define_table('professor',
                Field('first_name', required=True),
                Field('last_name', required=True)
                )

db.define_table('course',
                Field('subject', required=True),
                Field('nbr', label="number", required=True),
                Field('title', required=True),
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

db.define_table('subject',
                Field('name')
                )
