import webapp2
from google.appengine.api import mail
from google.appengine.ext.webapp import blobstore_handlers

import jinja2

# set default template directory
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('app/templates'))

# load custom libraries
from lib.basehandler import BaseHandler
import models
import forms


class GateHandler(BaseHandler):
    def get(self):

        """Display page to enter access code"""

        # if valid session, then redirect to welcome page
        if 'valid_user' in self.session:
            if self.session['valid_user'] is True:
                return self.redirect_to('welcome')

        template_values = {
            'cur_page': 'welcome',
            'csrf_token': BaseHandler.generate_csrf_token(self)
        }

        # validate access code if passed into URL
        if self.request.get('c'):
            is_valid = BaseHandler.validate_access_code(self, self.request.get('c'))

            # if access code is valid, redirect to Welcome page
            if is_valid is True:
                return self.redirect_to('welcome')
            else:
                template_values['code_attempted'] = True

        template = jinja_env.get_template('gate.html')
        self.response.out.write(template.render(template_values))

    def post(self):

        """Process access code entry"""

        if 'valid_user' in self.session:
            if self.session['valid_user'] is True:
                return self.redirect_to('welcome')

        template_values = {
            'cur_page': 'welcome',
            'code_attempted': True,
            'csrf_token': BaseHandler.generate_csrf_token(self)
        }

        is_valid = BaseHandler.validate_access_code(self, self.request.get('c'))

        if is_valid is True:
            return self.redirect_to('welcome')

        # re-display access code entry form
        template = jinja_env.get_template('gate.html')
        self.response.out.write(template.render(template_values))


class WelcomeHandler(BaseHandler):
    def get(self):

        """Display the Welcome page"""

        template_values = {
            'cur_page': 'welcome'
        }

        # load the welcome page template
        template = jinja_env.get_template('welcome.html')

        # display page
        self.response.out.write(template.render(template_values))


class RegisterHandler(BaseHandler):
    def get(self):

        """Display the Registration form for the first time"""

        form = forms.RegistrationForm()

        template_values = {
            'cur_page': 'register',
            'form': form,
            # 'user_type': self.session['user_type'],
            'csrf_token': BaseHandler.generate_csrf_token(self),
        }

        template = jinja_env.get_template('register.html')

        self.response.out.write(template.render(template_values))

    def post(self):

        """Validate the submitted Registration form

        If data is invalid, re-display form with errors.
        If data is valid, save data to db and re-direct to confirmation page.
        """

        template_values = {
            'cur_page': 'register',
            # 'user_type': self.session['user_type'],
            'csrf_token': BaseHandler.generate_csrf_token(self)
        }

        form = forms.RegistrationForm(self.request.POST)

        if self.request.method == 'POST' and form.validate():
            # process valid data

            # create new record
            registration = models.Registration()

            registration.first_name = form.first_name.data
            registration.last_name = form.last_name.data
            registration.email = form.email.data
            registration.company = form.company.data
            registration.industry = form.industry.data
            registration.help_with = form.help_with.data
            registration.share_my_info = form.share_my_info.data
            registration.access_code = self.session['access_code']
            # registration.user_type = self.session['user_type']

            """
            # add values specific to the 'agency' user type
            if self.session['user_type'] == 'agency':
                registration.company_brief = form.company_brief.data

                # if image was uploaded, upload the image to blobstore and save URL to db record
                uploaded_file = self.request.get(form.company_image.name)

                if uploaded_file:

                    # api for manipulating images
                    from google.appengine.api import images

                    # api for adding files to Google Cloud Storage
                    from google.appengine.api import files

                    image = images.Image(uploaded_file)

                    # set image type specifics
                    if image.format == images.JPEG:
                        # JPEG settings
                        file_settings = {
                            'suffix': '.jpg',
                            'mime_type': 'image/jpeg'
                        }
                    elif image.format == images.PNG:
                        # PNG settings
                        file_settings = {
                            'suffix': '.png',
                            'mime_type': 'image/png'
                        }
                    elif image.format == images.GIF:
                        # GIF settings
                        file_settings = {
                            'suffix': '.gif',
                            'mime_type': 'image/gif'
                        }

                    # make sure file is a supported image format
                    if file_settings:

                        # create an empty image file
                        writeable_file_name = files.blobstore.create(mime_type=file_settings['mime_type'])

                        # crop to original size (this is a hack so that we can use execute_transforms() to write the image to file)
                        image.crop(0.0, 0.0, 1.0, 1.0)

                        with files.open(writeable_file_name, 'a') as f:
                            f.write(image.execute_transforms())

                        # save file to blobstore
                        files.finalize(writeable_file_name)

                        # get the blob key for the newly created/hosted file
                        blob_key = files.blobstore.get_blob_key(writeable_file_name)

                        # add image url to registration record
                        registration.company_image = images.get_serving_url(blob_key)
            """

            # save registration record to datastore
            registration.put()

            # send a confirmation email to the user

            # =================================================================
            # TODO: Replace sender address with the address that should be used
            # =================================================================

            message = mail.EmailMessage()
            message.sender = "Agency Engage <engage-noreply@google.com>"
            message.to = registration.first_name + " " + registration.last_name + "<" + registration.email + ">"
            message.subject = "Thank you for registering"
            message.body = """
Thank you for registering, %s!

We will send out more details for the event as the date approaches.
            """ % (registration.first_name)

            message.send()

            # re-direct to confirmation page
            return self.redirect('register-complete')
        else:
            # data is invalid, re-display form
            template_values['form'] = form

        # render the page
        template = jinja_env.get_template('register.html')
        self.response.out.write(template.render(template_values))


class RegisterCompleteHandler(BaseHandler):
    def get(self):

        """Display Registration Complete page"""

        template_values = {
            'cur_page': 'register'
        }

        template = jinja_env.get_template('register-complete.html')
        self.response.out.write(template.render(template_values))


class TravelHandler(BaseHandler):
    def get(self):

        """Display the Travel page"""

        template_values = {
            'cur_page': 'travel'
        }

        template = jinja_env.get_template('travel.html')
        self.response.out.write(template.render(template_values))


class AgendaHandler(BaseHandler):
    def get(self):

        """Display the Agenda page"""

        template_values = {
            'cur_page': 'agenda'
        }

        template = jinja_env.get_template('agenda.html')
        self.response.out.write(template.render(template_values))


class AdminHandler(webapp2.RequestHandler):
    def get(self):

        """Admin for viewing registration data"""

        q = models.Registration.all()
        q.order("-date_added")
        registrations = q.run()

        template_values = {
            'registrations': registrations
        }

        template = jinja_env.get_template('admin.html')
        self.response.out.write(template.render(template_values))


class ExportRegistrationsHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):

        """Admin for viewing registration data"""

        import time
        import csv
        from google.appengine.api import files

        q = models.Registration.all()
        q.order("date_added")
        registrations = q.run()

        # get timestamp and remove milliseconds
        timestamp = str(time.time()).split('.')[0]
        output_file_name = 'engage-registrations_' + timestamp + '.csv'

        file_name = files.blobstore.create(mime_type='application/octet-stream')

        with files.open(file_name, 'a') as f:

            reg_writer = csv.writer(f, delimiter=',')

            reg_writer.writerow([
                'First Name',
                'Last Name',
                # 'User Type',
                'Company',
                'Email',
                'Industry',
                'I Want Help With',
                'Share Info',
                # 'Company Brief',
                'Access Code',
                'Date Added',
                # 'Company Image'
            ])

            for registration in registrations:

                if registration.share_my_info is True:
                    share_my_info = 'Yes'
                else:
                    share_my_info = 'No'

                reg_writer.writerow([
                    str(registration.first_name),
                    str(registration.last_name),
                    # str(registration.user_type),
                    str(registration.company),
                    str(registration.email),
                    str(registration.industry),
                    str(registration.help_with),
                    share_my_info,
                    # str(registration.company_brief),
                    str(registration.access_code),
                    str(registration.date_added).split('.')[0],
                    # str(registration.company_image)
                ])

        files.finalize(file_name)

        blob_key = files.blobstore.get_blob_key(file_name)

        # output the file to the browser
        self.response.headers['Content-Type'] = 'application/octet-stream'
        self.send_blob(blob_key, save_as=output_file_name)


class AddDummyValuesHandler(webapp2.RequestHandler):
    def get(self):

        """Add test data"""

        # only perform this handler if we're in debug mode
        if webapp2.get_app().debug is not True:
            self.abort(403)

        list = [
            '00SS1',
            '00SS2',
            '00SS3'
        ]

        for code in list:
            access_code = models.AccessCode()
            access_code.code = code
            access_code.put()

        self.response.out.write('Test data added.')

"""
class ClearDataHandler(webapp2.RequestHandler):

    def get(self):

        from google.appengine.ext import db

        db.delete(models.AccessCode.all())

        self.response.out.write('Access codes deleted')
        """
