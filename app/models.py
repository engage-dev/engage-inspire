from google.appengine.ext import db


class AccessCode(db.Model):
    code = db.StringProperty()
    # user_type = db.CategoryProperty(choices=['prospect', 'agency'])


class Registration(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    email = db.EmailProperty()
    company = db.StringProperty()
    industry = db.StringProperty()
    help_with = db.StringProperty()
    share_my_info = db.BooleanProperty()
    # company_brief = db.StringProperty(multiline=True)
    # company_image = db.StringProperty()
    # user_type = db.StringProperty()
    access_code = db.StringProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)
