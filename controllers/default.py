# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import json
from gluon.tools import geocode

def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def splash():
    return dict()

def aboutus():
    return dict()

def index():
    """
    This is your main controller.
    """
    # I am creating a bogus list here, just to have some divs appear in the
    # view.  You need to read at most 20 posts from the database, in order of
    # most recent first, and you need to return that list here.
    # Note that posts is NOT a list of strings in your actual code; it is
    # what you get from a db(...).select(...).
    # posts = ['banana', 'pear', 'eggplant']

    posts = db().select(
        orderby=~db.post.updated_on,
        limitby=(0, 5)
    )

    posts2 = db().select(
        orderby=~db.post_landlord.updatedon,
        limitby=(0, 5)
    )

    firstlast = get_user_name_from_email

    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()))
    if form.accepts(request):
        tokens = form.vars.name.split()
        query = reduce(lambda a,b:a&b,
                       [User.first_name.contains(k)|User.last_name.contains(k) \
                            for k in tokens])
        people = db(query).select(orderby=alphabetical)
    else:
        people = []

    return locals()

    return dict(form=form, posts=posts, posts2= posts2, username=get_user_name_from_email, firstlast=firstlast)

def profile():


    user = User(a0 or me)

    friends = db(User.id==Link.src)(Link.target==me).select(orderby=alphabetical)
    requests = db(User.id==Link.target)(Link.src==me).select(orderby=alphabetical)

    posts = db().select(
        orderby=~db.post.updated_on
    )

    posts2 = db().select(
        orderby=~db.post_landlord.updatedon
    )

    return locals()

def edit_mates():


    user = User(a0 or me)

    friends = db(User.id==Link.src)(Link.target==me).select(orderby=alphabetical)
    requests = db(User.id==Link.target)(Link.src==me).select(orderby=alphabetical)

    posts = db().select(
        orderby=~db.post.updated_on
    )

    posts2 = db().select(
        orderby=~db.post_landlord.updatedon
    )

    return locals()

def geo(form):
    (form.vars.longitude,form.vars.latitude)=geocode(form.vars.my_city+', USA')


# a page for searching friends and requesting friendship
@auth.requires_login()
def search():
    posts = db().select(
        orderby=~db.post_landlord.updatedon,
        limitby=(0, 5)
    )
    
    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()),
                          Field('search_county', label ='find users in your zip code'),
                          Field('search_states', label ='find users in your province')#,
                          #Field('search_email', label ='find users by email'),
                          )
    if form.accepts(request):
        tokens = form.vars.name.split()
        statee = form.vars.search_states
        countyy = form.vars.search_county
        #emaill = form.vars.search_email
        query = reduce(lambda a,b:a&b,
                       [User.first_name.contains(k)|User.last_name.contains(k) \
                            for k in tokens])
        query &= User.your_county.contains(countyy)
        query &= User.your_state.contains(statee)
        #query &= User.auth_user.email.contains(emaill)


        people = db(query).select(orderby=alphabetical)
    else:
        people = []
    


    return locals()

@auth.requires_login()
def edit():
    """
    This is the page to create / edit / delete a post.
    """

    p = None
    post_list = []
    if request.args(0) is None:
        # If argument zero in URL is empty then it must be a create form
        form_type = 'create'
        # Create form that enables insertion and name database table form refers to
        form = SQLFORM(db.post)
        # add cancel button
        form.add_button('cancel', URL('default', 'index'))
    else:
        # URL is referencing specific post
        # Check that post exists and if user is author of post
        # first() used to get either first element or none instead of iterator
        query = ((db.post.user_email == auth.user.email) &
                 (db.post.id == request.args(0)))

        p = db(query).select().first()
        if p is None:
            session.flash = T('Not Authorized')
            redirect(URL('default', 'index'))

        # Post now confirmed to be valid
        # Boolean to check user intent to edit, if not then just view
        is_edit = (request.vars.edit == 'true')
        form_type = 'edit' if is_edit else 'view'

        # Extract post content
        """post_list = None
        try:
            post_list = json.loads(p.post)
        except:
            pass
        if not isinstance(post_list, list):
            # When try causes error, execute here
            # If string in database then
            if isinstance(p.post, basestring):
                post_list = [p.post]
            else:
                post_list = []"""

        form = SQLFORM(db.post, record=p, deletable=is_edit, readonly=not is_edit, writable=is_edit)
        # add cancel button
        form.add_button('cancel', URL('default', 'index'))


        # Updates posts when edited
        # p.post_content = form.vars.post_content
        # Update created_on and updated_on date
        # Take time stamp of when post created only once, no need to update
        # p.created_on = datetime.datetime.utcnow()
        p.updated_on = datetime.datetime.utcnow()
        # Updates actual database
        p.update_record()

    # Add necessary buttons for each user action
    button_list = []
    if form_type == 'edit':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'create':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'view':
        button_list.append(A('Edit', _class='btn btn-warning',
                             _href=URL('default', 'edit', args=[p.id], vars=dict(edit='true'))))
        button_list.append(A('Back', _class='btn btn-primary',
                             _href=URL('default', 'index')))

    if form.process().accepted:
        # Post already validated and posted at this point
        # Update and insert record
        if form_type == 'create':
            session.flash = T('Post created!')
        else:
            session.flash = T('Content saved')
            p.post_content = form.vars.post_content
            p.min_budget = form.vars.min_budget
            p.max_budget = form.vars.max_budget
            p.number_of_people = form.vars.number_of_people
            p.description = form.vars.description
            p.my_city = form.vars.my_city
            p.longitude = ""
            p.latitude = ""
            (p.longitude,p.latitude) = geocode(form.vars.my_city+', United States')
            p.updated_on = datetime.datetime.utcnow()
            p.update_record()

        redirect(URL('default', 'index'))
    elif form.errors:
        (form.vars.longitude,form.vars.latitude) = ('','')
        session.flash = T('Get it right this time')

    # return dict(form=form, button_list=button_list, p=p, form_type=form_type, post_list=post_list)
    return locals()

@auth.requires_login()
def edit_Landlord():
    """
    This is the page to create / edit / delete a post.
    """
    p = None
    post_list = []
    if request.args(0) is None:
        # If argument zero in URL is empty then it must be a create form
        form_type = 'create'
        # Create form that enables insertion and name database table form refers to
        form = SQLFORM(db.post_landlord)
        # add cancel button
        form.add_button('cancel', URL('default', 'index'))
    else:
        # URL is referencing specific post
        # Check that post exists and if user is author of post
        # first() used to get either first element or none instead of iterator
        query = ((db.post_landlord.user_email == auth.user.email) &
                 (db.post_landlord.id == request.args(0)))

        p = db(query).select().first()
        if p is None:
            session.flash = T('Not Authorized')
            redirect(URL('default', 'index'))

        # Post now confirmed to be valid
        # Boolean to check user intent to edit, if not then just view
        is_edit = (request.vars.edit == 'true')
        form_type = 'edit' if is_edit else 'view'

        # Extract post content
        """post_list = None
        try:
            post_list = json.loads(p.post)
        except:
            pass
        if not isinstance(post_list, list):
            # When try causes error, execute here
            # If string in database then
            if isinstance(p.post, basestring):
                post_list = [p.post]
            else:
                post_list = []"""

        form = SQLFORM(db.post_landlord, record=p, deletable=is_edit, readonly=not is_edit, writable=is_edit)
        # add cancel button
        form.add_button('cancel', URL('default', 'index'))

        # Updates posts when edited
        # p.post_content = form.vars.post_content
        # Update created_on and updated_on date
        # Take time stamp of when post created only once, no need to update
        # p.created_on = datetime.datetime.utcnow()
        p.updatedon = datetime.datetime.utcnow()
        # Updates actual database
        p.update_record()

    # Add necessary buttons for each user action
    button_list = []
    if form_type == 'edit':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'create':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'view':
        button_list.append(A('Edit', _class='btn btn-warning',
                             _href=URL('default', 'edit', args=[p.id], vars=dict(edit='true'))))
        button_list.append(A('Back', _class='btn btn-primary',
                             _href=URL('default', 'index')))

    if form.process().accepted:
        # Post already validated and posted at this point
        # Update and insert record
        if form_type == 'create':
            session.flash = T('Post created!')
        else:
            session.flash = T('Content saved')
            p.my_address = form.vars.my_address
            p.my_city = form.vars.my_city
            p.my_state = form.vars.my_state
            p.sq_ft = form.vars.sq_ft
            p.num_bed = form.vars.num_bed
            p.num_bath = form.vars.num_bath
            p.washdry = form.vars.washdry
            p.furnish = form.vars.furnish
            p.pets = form.vars.pets
            p.more_info = form.vars.more_info
            p.picture = form.vars.picture
            p.longitude = ""
            p.latitude = ""
            (p.longitude,p.latitude) = geocode(form.vars.my_address+ form.vars.my_city+ form.vars.my_state + ', United States')
            p.updatedon = datetime.datetime.utcnow()
            p.update_record()

        redirect(URL('default', 'index'))
    elif form.errors:
        (form.vars.longitude,form.vars.latitude) = ('','')
        session.flash = T('Get it right this time')

    # return dict(form=form, button_list=button_list, p=p, form_type=form_type, post_list=post_list)
    return dict(form=form)

# using ajax to setup links
@auth.requires_login()
def housemate_link():
    if request.env.request_method!='POST': raise HTTP(400)
    if a0=='request' and not Link(src=a1,target=me):
        # insert a new friendship request
        Link.insert(src=me,target=a1)
    elif a0=='accept':
        # accept an existing friendship request
        db(Link.target==me)(Link.src==a1).update(accepted=True)
        if not db(Link.src==me)(Link.target==a1).count():
            Link.insert(src=me,target=a1)
    elif a0=='deny':
        # deny an existing friendship request
        db(Link.target==me)(Link.src==a1).delete()
    elif a0=='remove':
        # delete a previous friendship request
        db(Link.src==me)(Link.target==a1).delete()


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
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
