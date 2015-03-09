# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

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
    results = db(db.course.subject == subj.id).select()
    
    return dict(category=subj.title.title(), message=message, form=form, results=results)

def contact():
    return dict()
    

def termsandconditions():
    return dict()


def new():
    courseform = SQLFORM(db.course)
    subjectform = SQLFORM(db.subject)
    if courseform.process().accepted:
        redirect(URL('default', 'new'))
    if subjectform.process().accepted:
        redirect(URL('default', 'new'))
    return dict(courseform=courseform, subjectform=subjectform)


def professors():
    form = SQLFORM.factory(Field('search'))
    profs = ''
    if form.process().accepted:
        redirect(URL('default', 'professors', vars=dict(s=form.vars.search)))

    if request.vars.s != None:
        profs = db(((db.professor.last_name).lower() == (request.vars.s).lower()) | ((db.professor.first_name).lower() == (request.vars.s).lower()) ).select(orderby=db.professor.last_name)
    return dict(form=form, profs=profs)

def newprofessor():
    form = SQLFORM(db.professor)
    if form.process().accepted:
        nam = form.vars.first_name + ' ' + form.vars.last_name
        redirect(URL('default', 'professor', args=[nam]))
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
