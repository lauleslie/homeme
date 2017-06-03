# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime



# Create table to be called by SQLFORM
db.define_table('post',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('post_content', 'text'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow()),
                Field('min_budget'),
                Field('max_budget'),
                Field('number_of_people'),
                Field('description'),
                Field('my_city'),
                Field('latitude','double',writable=False),
                Field('longitude','double',writable=False)
                )

                #landlord stuff
db.define_table('post_landlord',
                 Field('user_email', default=auth.user.email if auth.user_id else None),
                 Field('createdon', 'datetime', default=datetime.datetime.utcnow()),
                 Field('updatedon', 'datetime', update=datetime.datetime.utcnow()),
                 Field('my_address'),
                 Field('my_city'),
                 Field('my_state'),
                 Field('sq_ft'),
                 Field('num_bed'),
                 Field('num_bath'),
                 Field('washdry', 'boolean'),
                 Field('furnish', 'boolean'),
                 Field('pets', 'boolean'),
                 Field('more_info', 'text'),
                 Field('picture', 'upload'),
                 Field('latitude','double',writable=False),
                 Field('longitude','double',writable=False)
                )




# a table to link two people
db.define_table('link',
                Field('src','reference auth_user'),
                Field('target','reference auth_user'),
                Field('accepted','boolean',default=False))

# a table designed to send an app to a person
db.define_table('app',
                Field('src','reference auth_user'),
                Field('target','reference auth_user'))

# and define some global variables that will make code more compact
User, Link, ApTab, Post = db.auth_user, db.link, db.app, db.post
me, a0, a1 = auth.user_id, request.args(0), request.args(1)
myfriends = db(Link.src==me)(Link.accepted==True)

myapps = db(ApTab.target==me)

alphabetical = User.first_name|User.last_name

def name_of(user): return '%(first_name)s %(last_name)s' % user


# I don't want to display the user email by default in all forms.
db.post.user_email.readable = db.post.user_email.writable = False
db.post.id.readable = db.post.id.writable = False
db.post.post_content.requires = IS_NOT_EMPTY()
db.post.created_on.readable = db.post.created_on.writable = False
db.post.updated_on.readable = db.post.updated_on.writable = False
db.post_landlord.createdon.readable = db.post_landlord.createdon.writable = False
db.post_landlord.updatedon.readable = db.post_landlord.updatedon.writable = False


db.post.min_budget.requires = IS_FLOAT_IN_RANGE(0,1000000000000)
db.post.max_budget.requires = IS_FLOAT_IN_RANGE(0,1000000000000)
db.post.number_of_people.requires = IS_INT_IN_RANGE(0,30)
db.post.description.requires = IS_NOT_EMPTY()
#db.post.budget.readable = db.post.budget.writable = False
#db.post.number_of_people.readable = db.post.number_of_people.writable = False
#db.post.description.readable = db.post.description.writable = False
# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
