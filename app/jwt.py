from typing import Dict, Optional

from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from sanic_jwt import BaseEndpoint, Initialize, exceptions
from sanic_jwt.initialization import endpoint_mappings, init_classes

from database import User

from .helpers import validators


class JWT(Initialize):
    def __init__(self, instance, app: Optional[Sanic] = None, **kwargs):  # pylint: disable=super-init-not-called
        for class_name in init_classes:
            if class_name in kwargs:
                value = kwargs.pop(class_name)
                setattr(self, class_name, value)

        app = self._Initialize__get_app(instance, app=app)

        self.app = app
        self.kwargs = kwargs
        self.instance = instance
        self.config = None
        self.bp = None

        self._Initialize__check_deprecated()
        self._Initialize__check_classes()
        self._Initialize__load_configuration()
        self._Initialize__initialize_bp()
        self._Initialize__load_responses()
        self._Initialize__add_endpoints()
        self._Initialize__initialize_instance()
        self._Initialize__initialize_claims()

    def _Initialize__add_endpoints(self):
        for mapping in endpoint_mappings:
            if all(map(self.config.get, mapping.keys)):
                self._Initialize__add_single_endpoint(
                    mapping.cls,
                    mapping.endpoint,
                    mapping.is_protected
                )

        self._Initialize__add_class_views()
        self.bp.exception(exceptions.SanicJWTException)(
            self.responses.exception_response
        )

        if not self.instance_is_blueprint:
            url_prefix = self._get_url_prefix()
            self.instance.blueprint(self.bp, url_prefix=url_prefix)

    def _Initialize__initialize_bp(self):
        super()._Initialize__initialize_bp()
        self.bp.strict_slashes = self.config.strict_slashes()


async def authenticate(request: Request) -> User:
    validators.raise_if_empty(request.json)
    login = request.json.get('login')
    password = request.json.get('password')
    breakpoint()
    if not login or not password:
        raise exceptions.AuthenticationFailed('Missing login or password.')

    user = await User.query.where(User.login == login).gino.first()
    if user:
        argon2 = request.app.argon2
        try:
            await argon2.async_verify(user.password, password)
        except argon2.exceptions.VerificationError:
            pass
        else:
            if await argon2.async_check_needs_rehash(user.password.decode('utf-8')):
                rehashed_password = await argon2.async_hash(password)
                await user.update(password=rehashed_password.encode('utf-8')).apply()
            return {'user_id': str(user.id), 'username': user.login}
    raise exceptions.AuthenticationFailed('Login or password is incorrect.')


async def retrieve_user(_, payload: Dict) -> User:
    user_id = payload.get('user_id')
    user = await User.query.where(User.id == user_id).gino.first()
    return user


class Logout(BaseEndpoint):
    async def post(self, request: Request, *args, **kwargs):  # pylint: disable=unused-argument
        if 'access_token' in request.cookies:
            response = json({'response': 'success'})
            del response.cookies['access_token']
            return response
        raise exceptions.MissingAuthorizationCookie('Missing access_token')
