from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class ApiKeyAuthentication(BaseAuthentication):

    def get_api_key_header(self, request):
        """
        Return request's 'x-api-key:' header, as a bytestring.

        Hide some test client ickyness where the header can be unicode.
        """
        api_key = None
        if 'x-api-key' in request.headers:
            api_key = request.headers['x-api-key']

        return api_key

    def authenticate(self, request):

        api_key = self.get_api_key_header(request)

        if not api_key:
            msg = _('Invalid header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(api_key)

    def authenticate_credentials(self, api_key):
        if api_key != settings.API_KEY:
            raise exceptions.AuthenticationFailed('Invalid Token')

    def authenticate_header(self, request):
        return 'Done'
