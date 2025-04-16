# fastapi-authlib-oidc
FastAPI OpenID authlib integration

## Installation

```bash
pip install fastapi-authlib-oidc
```

## Setup

- Secrets:
```yaml
client_id: CLIENT_ID
client_secret: CLIENT_SECRET
issuer: IDP_ISSUER <url before /.well-known/openid-configuration>
```

- Base login configuration

```python 
import json
import logging
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_oidc import FastAPIOIDC
from typing import Annotated
from starlette.datastructures import FormData
from pydantic import BaseModel

app = FastAPI()

app.extra.update(
    {
        "OIDC_CLIENT_SECRETS": "config/secrets.yml",
        "OIDC_OPENID_REALM": "OPENID",
        "OIDC_SCOPES": "openid email",
        "OIDC_INTROSPECTION_AUTH_METHOD": "client_secret_post",
        "OIDC_USER_INFO_ENABLED": True
    }
)

oidc = FastAPIOIDC(app)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class NotFound(BaseModel):
    details: str


async def authenticate(request: Annotated[Request, Depends()], ) -> JSONResponse:
    form_data: FormData = await request.form()
    user = oidc.token(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JSONResponse(content=json.loads(user.get_id()), status_code=status.HTTP_200_OK)


@app.get('/api/test/')
def index(token: Annotated[str, Depends(oauth2_scheme)]):
    logging.warning(oidc.user(token).email)
    return NotFound(details='Empty')

app.add_route(path='/token', route=authenticate, methods=["POST"], name='authenticate')

```

- Custom login configuration

```python
import json
import logging
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_oidc import FastAPIOIDC
from typing import Annotated
from starlette.datastructures import FormData
from pydantic import BaseModel

app = FastAPI()

app.extra.update(
    {
        "SSO_CLIENT_SECRETS": "config/secrets.yml",
        "SSO_OPENID_REALM": "OPENID",
        "SSO_SCOPES": "openid email",
        "SSO_INTROSPECTION_AUTH_METHOD": "client_secret_post",
        "SSO_USER_INFO_ENABLED": True
    }
)

oidc = FastAPIOIDC(app, prefix='SSO')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class NotFound(BaseModel):
    details: str


async def authenticate(request: Annotated[Request, Depends()], ) -> JSONResponse:
    form_data: FormData = await request.form()
    user = oidc.token(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JSONResponse(content=json.loads(user.get_id()), status_code=status.HTTP_200_OK)


@app.get('/api/test/')
def index(token: Annotated[str, Depends(oauth2_scheme)]):
    logging.warning(oidc.user(token).email)
    return NotFound(details='Empty')

app.add_route(path='/token', route=authenticate, methods=["POST"], name='authenticate')
```

## Using custom user model

Must be used after FastAPIOIDC.init_app() or FastAPIOIDC() if you are not using it

```python
oidc.user_model(UserModel)
```

See [user.py](https://github.com/frederickney/fastapi_authlib_oidc/blob/master/fastapi_oidc/user.py for more information about user model

## Custom login

Must be used after FastAPIOIDC.init_app() or FastAPIOIDC() if you are not using it

```python
def login(oidc_auth, model, token=None, user=None, password=None):
    """
    
    :param oidc_auth: oauth client
    :type oidc_auth: OAuth2Mixin
    :param model: user model
    :param token: user's oauth tokens 
    :type token: dict[str, any]
    :param user: username
    :type user: str
    :param password: user's password 
    :type password: str
    :return: 
    """
    pass

oidc.login_user(login)
```

## Custom client

Must be used after FastAPIOIDC.init_app() or FastAPIOIDC() if you are not using it

```python
def client(prefix):
    """

    :param prefix:
    :type prefix: str
    :return:
    :rtype: OAuth2Mixin
    """
    pass

oidc.client(client)
```

## Custom secret load

Must be used after FastAPIOIDC.init_app() or FastAPIOIDC() if you are not using it

```python
def secret(app, prefix):
    """

    :param app:
    :type app: flask.Flask
    :param prefix:
    :type prefix:str
    :return:
    :rtype: dict
    """
    pass

oidc.secret(secret)
```

Enjoy

# LICENSE

#### See [License file](LICENSE)
