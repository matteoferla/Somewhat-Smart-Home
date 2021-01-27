## For now matching a environ key is fine.

import os, logging
import pyramid.httpexceptions as exc

log = logging.getLogger(__name__)


class Authenticator:

    def __init__(self, request):
        self.request = request
        self.correct_key = os.environ['SECRETCODE']

    def has_key(self):
        """
        regardless of correct.

        :return:
        """
        if 'key' not in self.request.params:
            return False
        else:
            return True

    @property
    def given_key(self):
        if self.has_key():
            return self.request.params['key']
        else:
            return ''


    def is_valid(self):
        if self.given_key == self.correct_key:
            return True
        else:
            return False

    def assert_valid(self):
        if not self.has_key():
            log.info(f'Error authenticating (no authorisation key)')
            raise exc.HTTPBadRequest('No authorisation key (parameter key)')
        elif not self.is_valid():
            log.info(f'Error authenticating (wrong authorisation key)')
            raise exc.HTTPForbidden(f'Authorisation key {self.given_key} is wrong')
        else:
            return True