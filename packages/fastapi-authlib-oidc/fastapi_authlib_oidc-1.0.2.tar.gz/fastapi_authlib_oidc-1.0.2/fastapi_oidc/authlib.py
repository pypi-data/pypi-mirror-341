from werkzeug.local import LocalProxy
from authlib.integrations.base_client import FrameworkIntegration, BaseOAuth
from authlib.integrations.base_client import OAuthError

from fastapi_oidc.app import FastAPIAppOAuth2App, FastAPIAppOAuth1App


class FastAPIIntegration(FrameworkIntegration):

    @staticmethod
    def load_config(oauth, name, params):
        rv = {}
        for k in params:
            conf_key = f"{name}_{k}".upper()
            v = oauth.app.extra.get(conf_key, None)
            if v is not None:
                rv[k] = v
        return rv


class OAuth(BaseOAuth):
    oauth1_client_cls = FastAPIAppOAuth1App
    oauth2_client_cls = FastAPIAppOAuth2App
    framework_integration_cls = FastAPIIntegration

    def __init__(self, app=None, cache=None, fetch_token=None, update_token=None):
        super().__init__(
            cache=cache, fetch_token=fetch_token, update_token=update_token
        )
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app, cache=None, fetch_token=None, update_token=None):
        """Initialize lazy for Flask app. This is usually used for Flask application
        factory pattern.
        """
        self.app = app
        if cache is not None:
            self.cache = cache

        if fetch_token:
            self.fetch_token = fetch_token
        if update_token:
            self.update_token = update_token

        app.extensions = getattr(app, "extensions", {})
        app.extensions["fastapi_oidc.client.authlib"] = self

    def create_client(self, name):
        if not self.app:
            raise RuntimeError("OAuth is not init with Flask app.")
        return super().create_client(name)

    def register(self, name, overwrite=False, **kwargs):
        self._registry[name] = (overwrite, kwargs)
        if self.app:
            return self.create_client(name)
        return LocalProxy(lambda: self.create_client(name))


__all__ = [
    "OAuth",
    "FastAPIIntegration",
    "FastAPIAppOAuth1App",
    "FastAPIAppOAuth2App",
    "OAuthError",
]


