"""Flag Package Endpoints.
"""
from pytsite import auth as _auth, odm as _odm, http as _http, errors as _errors
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post(inp: dict, flag_type: str, model: str, uid: str) -> dict:
    """Create a flag.
    """
    try:
        c = _api.create(_odm.dispense(model, uid), _auth.get_current_user(), flag_type, float(inp.get('score', 1.0)))

        return {'count': c}

    except _odm.error.EntityNotFound:
        raise _http.error.NotFound("Entity '{}:{}' is not found".format(model, uid))

    except _errors.ForbidOperation as e:
        raise _http.error.Forbidden(str(e))


def patch(inp: dict, flag_type: str, model: str, uid: str) -> dict:
    """Toggle a flag.
    """
    try:
        author = _auth.get_current_user()
        entity = _odm.dispense(model, uid)
        count = _api.toggle(entity, author, flag_type, float(inp.get('score', 1.0)))

        return {
            'count': count,
            'status': _api.is_flagged(entity, author),
        }

    except _odm.error.EntityNotFound:
        raise _http.error.NotFound("Entity '{}:{}' is not found".format(model, uid))

    except _errors.ForbidOperation as e:
        raise _http.error.Forbidden(str(e))


def get(inp: dict, flag_type: str, model: str, uid: str) -> dict:
    """Get flag's status.
    """
    try:
        return {'status': _api.is_flagged(_odm.dispense(model, uid), _auth.get_current_user(), flag_type)}
    except _odm.error.EntityNotFound:
        return {'status': False}


def delete(inp: dict, flag_type: str, model: str, uid: str) -> dict:
    """Delete a flag.
    """
    try:
        return {'count': _api.delete(_odm.dispense(model, uid), _auth.get_current_user(), flag_type)}

    except _odm.error.EntityNotFound:
        raise _http.error.NotFound("Entity '{}:{}' is not found".format(model, uid))

    except _errors.ForbidOperation as e:
        raise _http.error.Forbidden(str(e))


def get_count(inp: dict, flag_type: str, model: str, uid: str) -> dict:
    """Set flag.
    """
    try:
        return {'count': _api.count(_odm.dispense(model, uid), flag_type)}
    except _odm.error.EntityNotFound:
        return {'count': 0}
