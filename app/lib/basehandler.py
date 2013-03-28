import webapp2
from webapp2_extras import sessions

from app.lib import utils

from app import models


class BaseHandler(webapp2.RequestHandler):
    """
        BaseHandler for all requests

        Holds the session properties so they
        are reachable for all requests
    """

    def dispatch(self):
        """
            Get a session store for this request.
        """
        # self.session_store = sessions.get_store(request=self.request)

        # if this is not the access code entry page,
        # check to see if this is a valid user session
        if self.request.path.startswith('/enter') is False:

            if 'valid_user' not in self.session:
                return self.redirect('/enter')

            if self.session['valid_user'] is not True:
                return self.redirect('/enter')

        try:
            # csrf protection
            if self.request.method == "POST":
                token = self.session.get('_csrf_token')
                if not token or token != self.request.get('_csrf_token'):
                    self.abort(403)

            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def generate_csrf_token(self):
        # session = sessions.get_store().get_session()
        # if '_csrf_token' not in self.session:
        self.session['_csrf_token'] = utils.random_string()
        return self.session['_csrf_token']

    def validate_access_code(self, access_code):

        # if not access_code.isdigit():
            # return False

        code_request = str(access_code)

        # validate access code
        if (code_request):

            q = models.AccessCode.all()
            q.filter('code =', code_request)
            result = q.get()

            if result:
                # access code is valid
                # save the code and/or user type to session cookie
                self.session['valid_user'] = True
                self.session['access_code'] = code_request
                # self.session['user_type'] = result.user_type
                return True
            else:
                return False
