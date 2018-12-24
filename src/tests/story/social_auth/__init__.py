class step(object):
    """
    Very dummy interface compatible with pytest-allure-adaptor
    To make shiny and pretty looking test cases reports you can replace step
    with allure.step without modifying test cases structure.

    The base idea to use this class is simple. To identify context blocks in
    test cases for user making test case reading easy.
    """
    def __init__(self, message):
        self.message = message

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            raise exc_val


class OAuth2MockMixin(object):
    """
    All oauth2 token initiate process looks almost the same from one platform
    for another. So basically this settings is template for any oauth2 backend
    test cases
    """

    oauth2_mock_scope = None
    oauth_response = {
        'code': 'ih2o4ibvirjxipejc19cevcp6b0939',
        'scope': 'channel.subscribers',
        'state': 'FakeState'
    }
    auth_response = {
        'access_token': '1e84e29qi5u2gozvoqaoebauwnd90n',
        'expires_in': 13048,
        'refresh_token': 'wrrjc22jp1gjm1irld1iklvaaaq1j77pemhgsi8pye6x1hlrdy',
        'scope': oauth2_mock_scope,
        'token_type': 'bearer'
    }
