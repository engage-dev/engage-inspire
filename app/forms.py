from wtforms import *


class AccessCodeForm(Form):
    code = TextField('code', [validators.required()])


class RegistrationForm(Form):
    first_name = TextField('first_name', [validators.required(), validators.Length(max=50)])
    last_name = TextField('first_name', [validators.required(), validators.Length(max=50)])
    email = TextField('email', [validators.required(), validators.Email(), validators.Length(max=100)])
    company = TextField('company', [validators.required(), validators.Length(max=200)])
    industry = SelectField('industry', [validators.required(), validators.NoneOf('0', 'Please select an industry')], choices=[
        ('0', 'Select one'),
        ('Automotive', 'Automotive'),
        ('Business-to-Business', 'Business-to-Business'),
        ('Consumer Goods', 'Consumer Goods'),
        ('Education', 'Education'),
        ('Financial Services', 'Financial Services'),
        ('Healthcare', 'Healthcare'),
        ('Media and Entertainment', 'Media and Entertainment'),
        ('Retail', 'Retail'),
        ('Technology', 'Technology'),
        ('Travel', 'Travel')
    ])
    help_with = SelectField('help_with', choices=[
        ('0', 'Select one'),
        ('Advanced AdWords Support', 'Advanced AdWords Support'),
        ('Advertising on Google', 'Advertising on Google'),
        ('An Enhanced Website', 'An Enhanced Website'),
        ('An online marketing plan', 'An online marketing plan'),
        ('Mobile and Video ads', 'Mobile and Video ads')
    ])
    share_my_info = BooleanField('share_my_info')
    # company_brief = TextAreaField('company_brief')
    # company_image = FileField('company_image')
