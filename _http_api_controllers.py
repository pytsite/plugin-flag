"""Pytsite Flag Plugin HTTP API Controllers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing as _routing, errors as _errors
from plugins import auth as _auth, odm as _odm
from . import _api


class Create(_routing.Controller):
    """Create a flag
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')
        score = float(self.arg('score', 1.0))

        try:
            return {'count': _api.create(_odm.get_by_ref(entity), _auth.get_current_user(), variant, score)}

        except _odm.error.EntityNotFound:
            raise self.not_found("Entity '{}' is not found".format(entity))

        except _errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class Status(_routing.Controller):
    """Get flag's status
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')

        try:
            return {'status': _api.is_flagged(_odm.get_by_ref(entity), _auth.get_current_user(), variant)}

        except _odm.error.EntityNotFound:
            return {'status': False}


class Toggle(_routing.Controller):
    """Toggle a flag
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')
        score = float(self.arg('score', 1.0))

        try:
            author = _auth.get_current_user()
            entity = _odm.get_by_ref(entity)
            count = _api.toggle(entity, author, variant, score)

            return {
                'count': count,
                'status': _api.is_flagged(entity, author, variant),
            }

        except _odm.error.EntityNotFound:
            raise self.not_found("Entity '{}' is not found".format(entity))

        except _errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class Delete(_routing.Controller):
    """Delete a flag
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')

        try:
            return {'count': _api.delete(_odm.get_by_ref(entity), _auth.get_current_user(), variant)}

        except _odm.error.EntityNotFound:
            raise self.not_found("Entity '{}' is not found".format(entity))

        except _errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class Count(_routing.Controller):
    """Get flags count
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')

        try:
            return {'count': _api.count(_odm.get_by_ref(entity), variant)}
        except _odm.error.EntityNotFound:
            return {'count': 0}
