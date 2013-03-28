from webapp2_extras.routes import RedirectRoute
import handlers

_routes = [
    RedirectRoute('/enter', handlers.GateHandler, name='enter', strict_slash=True),
    RedirectRoute('/register', handlers.RegisterHandler, name='register', strict_slash=True),
    RedirectRoute('/register-complete', handlers.RegisterCompleteHandler, name='register_complete', strict_slash=True),
    RedirectRoute('/agenda', handlers.AgendaHandler, name='agenda', strict_slash=True),
    RedirectRoute('/travel', handlers.TravelHandler, name='travel', strict_slash=True),
    RedirectRoute('/admin', handlers.AdminHandler, name='admin', strict_slash=True),
    RedirectRoute('/admin/download-csv', handlers.ExportRegistrationsHandler, name='download_csv', strict_slash=True),
    RedirectRoute('/dummydata', handlers.AddDummyValuesHandler, name='dummydata', strict_slash=True),
    # RedirectRoute('/clear-data', handlers.ClearDataHandler, name='clear_data', strict_slash=True),
    RedirectRoute('/', handlers.WelcomeHandler, name='welcome', strict_slash=True)
]

# example route with passthru variable
# RedirectRoute('/social_login/<provider_name>/complete', handlers.CallbackSocialLoginHandler, name='social-login-complete', strict_slash=True),


def get_routes():
    return _routes


def add_routes(app):
    for r in _routes:
        app.router.add(r)
