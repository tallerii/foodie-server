import requests
from foodie.users.models import User
from django.conf import settings

class FacebookBackend:
    APP_ACCESS_TOKEN = None

    def authenticate(self, request, token, FCMToken):
        app_token = self.get_app_token()
        res = self.get('debug_token', access_token=app_token, params={'input_token': token})

        print(res.json())

        if not res.json().get('data').get('is_valid'):
            return None

        user_id = res.json().get('data').get('user_id')
        res = self.get(
            user_id,
            access_token=token,
            params={
                'fields': 'first_name, last_name, email'
            }
        )

        if not (res.json().get('email') and res.json().get('first_name') and res.json().get('last_name')):
            return None

        try:
            user = User.objects.get(email=res.json().get('email'))
        except User.DoesNotExist:
            # Create a new user.
            user = User(
                email=res.json().get('email'),
                first_name=res.json().get('first_name'),
                last_name=res.json().get('last_name'),
                FCMToken=FCMToken
            )
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def get_app_token(self):
        if self.APP_ACCESS_TOKEN is None:
            res = self.get(
                'oauth/access_token',
                access_token=None,
                params={
                    'client_id': settings.FACEBOOK_APP_ID,
                    'client_secret': settings.FACEBOOK_APP_SECRET,
                    'grant_type': 'client_credentials'
                }
            )
            self.APP_ACCESS_TOKEN = res.json()['access_token']
        return self.APP_ACCESS_TOKEN

    def get(self, endpoint, access_token=None, params={}):
        FACEBOOK_API_ROOT = 'https://graph.facebook.com/'
        FACEBOOK_API_VERSION = 'v4.0/'
        if access_token is not None:
            params['access_token'] = access_token
        return requests.get(
            FACEBOOK_API_ROOT + FACEBOOK_API_VERSION + endpoint,
            params=params
        )
