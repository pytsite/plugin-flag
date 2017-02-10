"""Flag Package Endpoints.
"""
from pytsite import auth as _auth, odm as _odm, http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _check_permissions() -> _auth.model.AbstractUser:
    user = _auth.get_current_user()
    if user.is_anonymous:
        raise _http.error.Unauthorized()

    return user


def get_status(inp: dict, flag_type: str, model: str, uid: str) -> dict:
    """Set flag.
    """
    author = _check_permissions()

    try:
        return {'status': _api.is_flagged(_odm.dispense(model, uid), author, flag_type)}
    except _odm.error.EntityNotFound:
        return {'status': False}


def get_count(inp: dict, flag_type: str, model: str, uid: str) -> dict:
    """Set flag.
    """
    _check_permissions()

    try:
        return {'count': _api.count(_odm.dispense(model, uid), flag_type)}
    except _odm.error.EntityNotFound:
        return {'count': 0}


def patch(inp: dict, flag_type: str, model: str, uid: str) -> dict:
    """Toggle flag.
    """
    author = _check_permissions()

    try:
        entity = _odm.dispense(model, uid)
        count = _api.toggle(entity, author, flag_type, float(inp.get('score', 1.0)))

        return {
            'count': count,
            'status': _api.is_flagged(entity, author),
        }

    except _odm.error.ForbidEntityOperation as e:
        raise _http.error.Forbidden(str(e))
