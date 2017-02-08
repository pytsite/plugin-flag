"""Flag Package Endpoints.
"""
from pytsite import auth as _auth, odm as _odm, http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def patch_toggle(inp: dict, model: str, uid: str) -> dict:
    """Set/remove flag.
    """
    # Check for permissions
    if _auth.get_current_user().is_anonymous:
        raise _http.error.Unauthorized()

    try:
        entity = _odm.dispense(model, uid)
        count = _api.toggle(entity)

        return {
            'count': count,
            'status': _api.is_flagged(entity),
        }

    except _odm.error.ForbidEntityOperation as e:
        raise _http.error.Forbidden(str(e))
