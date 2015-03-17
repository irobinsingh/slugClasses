# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def get_full_name():
    name = 'anonymous'
    if auth.user:
        name = auth.user.first_name + ' ' +auth.user.last_name
    return name

def review():
    form = ''
    message = ''
    if request.args(1) == 'error':
        message = 'ERROR: class not found'
    if(request.args(0) == 'class'):
        form= SQLFORM.factory(
                              Field('professor', db.professor, requires = IS_IN_DB(db, 'professor.id', '%(last_name)s, %(first_name)s')),
                              Field('summary'),
                              Field('body', 'text'),)
        subj = db(db.subject.acronym.lower() == request.vars.s.lower()).select()
        clss = db((db.course.nbr == request.vars.n) & (db.course.subject == subj.first())).select().first()
        if form.process().accepted:
            db.revision.insert(course_id = clss.id, professor_id = form.vars.professor, author=get_full_name(), date_created=datetime.utcnow(), summary=form.vars.summary, body=form.vars.body)
            redirect(URL('default', 'classes'))
    
    if(request.args(0) == 'professor'):
        form= SQLFORM.factory(
                              Field('subject', db.subject, requires = IS_IN_DB(db, 'subject.id', '%(acronym)s: %(title)s')),
                              Field('nbr', label="number"),
                              Field('summary'),
                              Field('body', 'text'),)
        if form.process().accepted:
            clss = db((db.course.nbr == form.vars.nbr) & (db.course.subject == form.vars.subject)).select().first()
            prof = db((db.professor.last_name.lower() == request.vars.l.lower()) & (db.professor.first_name.lower() == request.vars.f.lower())).select().first()
            if clss == None:
                redirect(URL('default', 'review', args=[request.args(0), 'error'], vars=dict(l=request.vars.l, f=request.vars.f, s=request.vars.s, n=request.vars.n)))
            db.revision.insert(course_id = clss.id, professor_id = prof.id, author=get_full_name(), date_created=datetime.utcnow(), summary=form.vars.summary, body=form.vars.body)
            redirect(URL('default', 'professor', vars=dict(l=request.vars.l, f=request.vars.f)))
    return dict(form=form, message=message)

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))

def classes():
    form = SQLFORM.factory(Field('subject', required=True), Field('number', 'integer', required=True))
    message = ''
    results = ''
    if form.process().accepted:
        if(form.vars.subject == None or form.vars.number == None):
            message = 'Error, please enter a valid search query.'
            if(request.args(0) == 'search'):
                redirect(URL('default', 'classes'))
        else:
            redirect(URL('default', 'classes', args=['search'], vars=dict(course=form.vars.subject, number=form.vars.number)))
        
    if request.args(0) == 'search' and request.vars.course != None and request.vars.number!= None:
        subj = db(db.subject.acronym.lower() == request.vars.course.lower()).select()
        if len(subj)>0:
            results = db((db.course.nbr == request.vars.number) & (db.course.subject == subj.first()) ).select(orderby=db.course.nbr)
        else:
            results = []
    
    sbjcts = db().select(db.subject.ALL, orderby=db.subject.acronym)
    return dict(sbjcts=sbjcts, form=form, message=message, results=results)

def course():
    subj = db(db.subject.acronym.lower() == request.vars.s.lower()).select()
    clss = ''
    reviews = []
    if len(subj)>0:
        clss = db((db.course.nbr == request.vars.n) & (db.course.subject == subj.first()) ).select().first()

    if clss != '':
        reviews = db(db.revision.course_id == clss.id).select(orderby=~db.revision.date_created)
    return dict(form=reviews)

def professor():
    prof = ''
    if request.vars.l != None and request.vars.f != None:
        prof = db((db.professor.last_name.lower() == request.vars.l.lower()) & (db.professor.first_name.lower() == request.vars.f.lower())).select().first()
   
    reviews = []
    if prof != '':
        reviews = db(db.revision.professor_id == prof.id).select(orderby=~db.revision.date_created)
    return dict(form=reviews)


def subject():
    form = SQLFORM.factory(Field('subject', required=True), Field('number', 'integer', required=True))
    results = ''
    message = ''
    if form.process().accepted:
        if(form.vars.subject == None or form.vars.number == None):
            message = 'Error, please enter a valid search query.'
            if(request.args(0) == 'search'):
                redirect(URL('default', 'classes'))
        else:
            redirect(URL('default', 'classes', args=['search'], vars=dict(course=form.vars.subject, number=form.vars.number)))
    
    subj = db(db.subject.acronym.lower() == request.args(0).lower()).select().first()
    results = db(db.course.subject == subj.id).select(orderby=db.course.nbr)
    
    return dict(category=subj.title.title(), message=message, form=form, results=results)

def contact():
    return dict()
    

def termsandconditions():
    return dict()

@auth.requires_login()
def new():
    courseform = SQLFORM(db.course)
    subjectform = SQLFORM(db.subject)
    if courseform.process().accepted:
        redirect(URL('default', 'new', vars=dict(s=True)))
    if subjectform.process().accepted:
        redirect(URL('default', 'new', vars=dict(s=True)))
    return dict(courseform=courseform, subjectform=subjectform)


def professors():
    form = SQLFORM.factory(Field('search'))
    profs = ''
    if form.process().accepted:
        redirect(URL('default', 'professors', vars=dict(s=form.vars.search)))

    if request.vars.s != None:
        profs = db(((db.professor.last_name).lower() == (request.vars.s).lower()) | ((db.professor.first_name).lower() == (request.vars.s).lower()) ).select(orderby=db.professor.last_name)
    return dict(form=form, profs=profs)

@auth.requires_login()
def newprofessor():
    form = SQLFORM(db.professor)
    if form.process().accepted:
        nam = form.vars.first_name + ' ' + form.vars.last_name
        redirect(URL('default', 'professor', vars=dict(f=form.vars.first_name, l=form.vars.last_name)))
    return dict(form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
