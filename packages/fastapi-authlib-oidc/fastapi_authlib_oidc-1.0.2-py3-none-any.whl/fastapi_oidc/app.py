import logging
import requests

from authlib.integrations.base_client import OAuth1Mixin, BaseApp, OAuthError, OAuth2Mixin, OpenIDMixin
from authlib.integrations.requests_client import OAuth1Session, OAuth2Session
from fastapi import HTTPException, status


class FastAPIAppOAuth1App(OAuth1Mixin, BaseApp):
    client_cls = OAuth1Session

    def authorize_access_token(self, **kwargs):
        pass

class FastAPIAppOAuth2App(OAuth2Mixin, OpenIDMixin, BaseApp):
    client_cls = OAuth2Session

    def parse_access_token(self, token, nonce, claims_options=None, claims_cls=None, leeway=120):
        if type(token) is dict:
            if 'id_token' not in token and 'access_token' in token:
                token['id_token'] = token['access_token']
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return super(FastAPIAppOAuth2App, self).parse_id_token(
                token,
                nonce,
                claims_options,
                claims_cls,
                leeway=leeway
            )
        else:
            response = requests.get(
                self.load_server_metadata()['userinfo_endpoint'],
                headers={'Authorization': f'Bearer {token}'}
            )
            if response.ok:
                user_profile = response.json()
                return user_profile
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )


    def authorize_access_token(self, **kwargs):
        pass
