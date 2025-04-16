# coding: utf-8

__author__ = "Frédérick NEY"

import base64
import datetime
import inspect
import json
import yaml
import logging
import warnings

from typing import Annotated

import requests
from authlib.integrations.base_client import OAuthError, OAuth2Mixin
from authlib.jose import jwt, JsonWebToken
from authlib.oauth2.rfc7662 import (
    IntrospectTokenValidator as BaseIntrospectTokenValidator,
)
from authlib.oidc.core import CodeIDToken, ImplicitIDToken
from fastapi import Depends, HTTPException, status
from starlette.datastructures import FormData
from werkzeug.utils import import_string

from .authlib import OAuth
from .user import OpenIDUser


def _get_client(app, prefix):
    """

    :param app:
    :type app: fastapi.FastAPI
    :param prefix:
    :type prefix: str
    :return:
    :rtype: OAuth2Mixin
    """
    oauth = app.extensions.get(prefix.lower(), None)
    if oauth:
        oauth.register(
            name=prefix.lower(),
            server_metadata_url=app.extra["{}_SERVER_METADATA_URL".format(prefix)],
            client_kwargs={
                "scope": app.extra["{}_SCOPES".format(prefix)],
                "token_endpoint_auth_method": app.extra[
                    "{}_INTROSPECTION_AUTH_METHOD".format(prefix)
                ],
            },
        )
        return getattr(oauth, prefix.lower())
    else:
        raise Exception("{}: oauth client not set".format(__name__))


def _load_secrets(app, prefix):
    """

    :param app:
    :type app: fastai.FastAPI
    :param prefix:
    :type prefix:str
    :return:
    :rtype: dict
    """
    # Load client_secrets.json to pre-initialize some configuration
    content_or_filepath = app.extra["{}_CLIENT_SECRETS".format(prefix)]
    if isinstance(content_or_filepath, dict):
        return content_or_filepath
    else:
        with open(content_or_filepath) as f:
            return yaml.load(f, yaml.FullLoader)


def _full_openid_profile(oidc_auth, token):
    """

    :param oidc_auth: auth client
    :type oidc_auth: OAuth2Mixin
    :param token: user's oauth token
    :type token: dict
    :return:
    """
    if 'access_token' in token:
        load_key = oidc_auth.create_load_key()
        claims_params = dict(
            nonce=token.get('nonce', ''),
            client_id=oidc_auth.client_id,
        )
        if 'access_token' in token:
            claims_params['access_token'] = token['access_token']
            claims_cls = CodeIDToken
        else:
            claims_cls = ImplicitIDToken
        metadata = oidc_auth.load_server_metadata()
        claims_options = {'iss': {'values': [metadata['issuer']]}}

        alg_values = metadata.get('id_token_signing_alg_values_supported')
        if alg_values:
            _jwt = JsonWebToken(alg_values)
        else:
            _jwt = jwt
        claims = _jwt.decode(
            token['access_token'], key=load_key,
            claims_cls=claims_cls,
            claims_options=claims_options,
            claims_params=claims_params,
        )
        return claims
    return None


def _logout_oidc_user(oidc_auth):
    """

    :param oidc_auth: auth client
    :type oidc_auth: OAuth2Mixin
    :return:
    """
    logging.debug("{}: logged out".format(__name__))


def _token(token):
    """

    :param token: user's oauth token
    :type token: dict
    :return:
    """
    if 'access_token' in token:
        return {
            "token": {
                "access_token": token['access_token'],
                "expires_in": token['expires_in'],
                "refresh_expires_in": token['refresh_expires_in'],
                "refresh_token": token['refresh_token'],
                "token_type": token['token_type'],
                "id_token": token['id_token'],
                "not-before-policy": token['not-before-policy'],
                "session_state": token['session_state'],
                "scope": token['scope'],
                "expires_at": token.get('expires_at', datetime.datetime.now().timestamp() + token['expires_in'])
            }
        }
    else:
        return {
            "token": {
                "expires_in": token['expires_in'],
                "refresh_expires_in": token['refresh_expires_in'],
                "refresh_token": token['refresh_token'],
                "token_type": token['token_type'],
                "id_token": token['id_token'],
                "not-before-policy": token['not-before-policy'],
                "session_state": token['session_state'],
                "scope": token['scope'],
                "expires_at": token.get('expires_at', datetime.datetime.now().timestamp() + token['expires_in'])
            }
        }


def _login_oidc_user(oidc_auth, model, token=None, user=None, password=None):
    """

    :param oidc_auth: oauth client
    :type oidc_auth: fastapi_oidc.app.FastAPIAppOAuth2App
    :param model: user model
    :param token: user's oauth token
    :return:
    """
    if token:
        if 'userinfo' in token:
            if 'nonce' in token['userinfo']:
                token['nonce'] = token['userinfo']['nonce']
        try:
            full_profile = _full_openid_profile(oidc_auth, token)
            if full_profile:
                full_profile.update(_token(token))
                user = model(**full_profile)
                return user
        except KeyError as e:
            logging.warning(e)
            if 'userinfo' in token:
                profile = token['userinfo']
                profile.update(_token(token))
                user = model(**profile)
                return user
    if user and password:
        response = requests.post(oidc_auth.load_server_metadata()['token_endpoint'], headers={
            'Authorization': 'Basic {}'.format(
                base64.b64encode(
                    "{}:{}".format(oidc_auth.client_id, oidc_auth.client_secret).encode('utf-8')
                ).decode('utf-8')
            )
        }, data={'username': user, 'password': password, 'grant_type': 'password'})
        if response.ok:
            user = None
            try:
                token = response.json()
                if 'id_token' not in token and 'access_token' in token:
                    token['id_token'] = token['access_token']
                full_profile = _full_openid_profile(oidc_auth, token)
                if full_profile:
                    full_profile.update(_token(token))
                    user = model(**full_profile)
                    return user
            except KeyError as e:
                import traceback
                logging.warning(e)
                logging.debug(traceback.format_exc(e))
                if 'userinfo' in token:
                    profile = token['userinfo']
                    profile.update(_token(token))
                    user = model(**profile)
                    return user
            return user
        else:
            logging.error(response.json())
        return None


class IntrospectTokenValidator(BaseIntrospectTokenValidator):
    flask_oidc = None

    def __init__(self, flask_oidc):
        self.flask_oidc = flask_oidc
        super(IntrospectTokenValidator, self).__init__()

    """Validates a token using introspection."""

    def introspect_token(self, token_string):
        """Return the token introspection result."""
        oauth = self.flask_oidc.oidc_prepare(self.flask_oidc.token)
        metadata = oauth.load_server_metadata()
        if "introspection_endpoint" not in metadata:
            raise RuntimeError(
                "Can't validate the token because the server does not support "
                "introspection."
            )
        with oauth._get_oauth_client(**metadata) as session:
            response = session.introspect_token(
                metadata["introspection_endpoint"], token=token_string
            )
        return response.json()


class FastAPIOIDC(object):
    _logout_user = None
    _login_user = None
    _error = None
    _get_client = None
    _user_model = OpenIDUser
    load_secrets = None

    def __init__(self, app=None, prefix='OIDC'):
        self.client_secrets = None
        self._prefix = prefix.upper()
        self._login_user = _login_oidc_user
        self._logout_user = _logout_oidc_user
        self._get_client = _get_client
        self.load_secrets = _load_secrets
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """

        :param app:
        :type app: fastapi.FastAPI
        """
        self._app = app
        secrets = self.load_secrets(app, self._prefix)
        self.client_secrets = secrets
        app.extra.setdefault("{}_CLIENT_ID".format(self._prefix), self.client_secrets["client_id"])
        app.extra.setdefault(
            "{}_CLIENT_SECRET".format(self._prefix), self.client_secrets["client_secret"]
        )
        app.extra.setdefault("{}_USER_INFO_ENABLED".format(self._prefix), True)
        app.extra.setdefault("{}_INTROSPECTION_AUTH_METHOD".format(self._prefix), "client_secret_post")
        app.extra.setdefault("{}_CLOCK_SKEW".format(self._prefix), 60)
        app.extra.setdefault("{}_RESOURCE_SERVER_ONLY".format(self._prefix), False)
        app.extra.setdefault("{}_CALLBACK_ROUTE".format(self._prefix), None)
        app.extra.setdefault("{}_OVERWRITE_REDIRECT_URI".format(self._prefix), None)

        app.extra.setdefault("{}_SCOPES".format(self._prefix), "openid email")
        if "openid" not in app.extra["{}_SCOPES".format(self._prefix)]:
            raise ValueError('The value "openid" must be in the {}_SCOPES'.format(self._prefix))
        if isinstance(app.extra["{}_SCOPES".format(self._prefix)], (list, tuple)):
            warnings.warn(
                "The {}_SCOPES configuration value should now be a string".format(self._prefix),
                DeprecationWarning,
                stacklevel=2,
            )
            app.extra["{}_SCOPES".format(self._prefix)] = " ".join(app.extra["{}_SCOPES".format(self._prefix)])

        provider_url = self.client_secrets["issuer"].rstrip("/")
        app.extra.setdefault(
            "{}_SERVER_METADATA_URL".format(self._prefix),
            f"{provider_url}/.well-known/openid-configuration",
        )
        # Register configuration on app so we can retrieve it later on
        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}
        if self._prefix.lower() not in app.extensions.keys():
            app.extensions[self._prefix.lower()] = OAuth(app)

        # User model
        app.extra.setdefault("{}_USER_CLASS".format(self._prefix), "fastapi_oidc.user.OpenIDUser")
        if app.extra["{}_USER_CLASS".format(self._prefix)]:
            self._user_model = import_string(
                app.extra["{}_USER_CLASS".format(self._prefix)]
            )

    def client(self, callback):
        if callable(callback) and not inspect.isclass(callback):
            self._get_client = callback
        else:
            raise Exception("{}.{}.client: {} not callable".format(__name__, __class__.__name__, callback))

    def oidc_prepare(self):
        """

        :return:
        :rtype: fastapi_oidc.app.FastAPIAppOAuth2App
        """
        client = self._get_client(self._app, self._prefix)
        return client


    def user(self, token):
        """

        :param xml_assertion:
        :return: logged in user
        """
        if token is not None:
            oauth_client = self.oidc_prepare()
            if hasattr(self._user_model, 'load_from_access_token'):
                return self._user_model.load_from_access_token(oauth_client, token)
            else:
                logging.warning("{}.{}.user_model: {} has no attribute load_from_access_token".format(
                    __name__,
                    __class__.__name__,
                    self._user_model
                ))
                return OpenIDUser.load_from_access_token(oauth_client, token)
        return None

    def user_model(self, model):
        if inspect.isclass(model):
            self._user_model = model
        else:
            raise Exception("{}.{}.user_model: {} not a class".format(__name__, __class__.__name__, model))

    def login_user(self, callback):
        if callable(callback) and not inspect.isclass(callback):
            self._login_user = callback
        else:
            raise Exception("{}.{}.login_user: {} not callable".format(__name__, __class__.__name__, callback))


    def secret(self, callback):
        if callable(callback) and not inspect.isclass(callback):
            self.load_secrets = callback
        else:
            raise Exception("{}.{}.logout_user: {} not callable".format(__name__, __class__.__name__, callback))

    def token(self, form_data: Annotated[FormData, Depends()]):
        """

        :param form_data:
        :type form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
        :return:
        :rtype: OpenIDUser
        """
        logging.debug('Received login')
        try:
            oauth_client = self.oidc_prepare()
            oauth_client.authorize_access_token()
        except OAuthError as e:
            logging.exception("Could not get the access token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not get access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = self._login_user(
            oauth_client, self._user_model,
            password = form_data.get("password"),
            user = form_data.get("username")
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
