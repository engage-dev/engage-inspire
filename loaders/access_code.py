#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.tools import bulkloader
from app.models import AccessCode


class AccessCodeLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'AccessCode',
            [('code', str),
            ('user_type', str)
            ])

loaders = [AccessCodeLoader]

# to load data into datastore, use the following command
# appcfg.py upload_data --config_file=loaders/access_code.py --filename=_source/dummy.csv --kind=AccessCode --url=http://localhost:8081/_ah/remote_api