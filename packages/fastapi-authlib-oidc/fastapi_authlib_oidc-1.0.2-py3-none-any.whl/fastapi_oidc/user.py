# coding: utf-8

__author__ = "Frédérick NEY"

import json
import logging
from base64 import b64encode
from datetime import datetime

import authlib.jose.errors
import requests


class OpenIDUser(object):

    @staticmethod
    def load_from_token(oidc_auth, token):
        """

        :param oidc_auth:
        :type oidc_auth: fastapi_oidc.app.FastAPIAppOAuth2App
        :param token:
        :return:
        """
        token = token.replace("'", '"')
        if type(token) is str:
            token = json.loads(token)
            try:
                if 'id_token' in token:
                    userinfo = oidc_auth.parse_id_token(token, nonce="")
                    userinfo["token"] = token
                    user = OpenIDUser(**userinfo)
                    if not user.is_authenticated:
                        refresh = requests.post(oidc_auth.load_server_metadata()['token_endpoint'], data={
                            'grant_type': "refresh_token",
                            'refresh_token': token['refresh_token']
                        }, headers={
                            'Authorization': "Basic {}".format(b64encode("{}:{}".format(
                                oidc_auth.client_id, oidc_auth.client_secret
                            ).encode()).decode('utf-8'))
                        })
                        token = refresh.json()
                        userinfo = oidc_auth.parse_id_token(token, nonce="")
                        userinfo["token"] = token
                        user = OpenIDUser(**userinfo)
                    return user
            except authlib.jose.errors.ExpiredTokenError as e:
                # next ?
                pass
        return None

    @staticmethod
    def load_from_access_token(oidc_auth, token):
        """

        :param oidc_auth:
        :type oidc_auth: fastapi_oidc.app.FastAPIAppOAuth2App
        :param token:
        :type token: str
        :return:
        :rtype: OpenIDUser
        """
        user_profile = oidc_auth.parse_access_token(token, nonce="")
        user_profile.update({'token': {'access_token': token}})
        return OpenIDUser(**user_profile)


    def __init__(self, **kwargs):
        for key, attr in kwargs.items():
            setattr(self, key, str(attr))

    def get_id(self):
        if hasattr(self, "token"):
            if type(self.token) is str:
                return self.token.replace("'", '"')
            return self.token

    @property
    def is_active(self):
        if hasattr(self, "email_verified"):
            return getattr(self, 'email_verified')
        return False

    @property
    def is_authenticated(self):
        if hasattr(self, "exp"):
            return datetime.fromtimestamp(
                int(getattr(self, 'exp'))
            ).strftime("%Y-%m-%dT%H:%M:%S.%fZ") >= datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return False

    @property
    def is_anonymous(self):
        if hasattr(self, "email_verified"):
            return not getattr(self, 'email_verified')
        return False
