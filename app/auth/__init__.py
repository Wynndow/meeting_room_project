from flask import Blueprint

from ..authentication import requires_authentication

auth = Blueprint('auth', __name__)

auth.before_request(requires_authentication)

from . import views  # noqa
