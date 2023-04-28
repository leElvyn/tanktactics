from urllib.parse import urlparse
from social_core.backends.open_id import OpenIdAuth
from social_core.exceptions import AuthMissingParameter


class ProloginOpenId(OpenIdAuth):
    """Prologin internal OpenID authentication backend"""
    name = 'prologin'
    URL = "http://demo.c2id.com/oidc-client"

    def get_user_details(self, response):
        """Generate username from identity url"""
        values = super(ProloginOpenId, self).get_user_details(response)
        values['username'] = values.get('username') or \
                             urlparse.urlsplit(response.identity_url)\
                                        .netloc.split('.', 1)[0]
        return values
