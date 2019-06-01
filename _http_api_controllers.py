"""Pytsite Flag Plugin HTTP API Controllers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import routing, errors
from plugins import auth, odm
from . import _api


class Create(routing.Controller):
    """Create a flag
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')
        score = float(self.arg('score', 1.0))

        try:
            return {'count': _api.create(odm.get_by_ref(entity), auth.get_current_user(), variant, score)}

        except odm.error.EntityNotFound:
            raise self.not_found("Entity '{}' is not found".format(entity))

        except errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class Status(routing.Controller):
    """Get flag's status
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')

        try:
            return {'status': _api.is_flagged(odm.get_by_ref(entity), auth.get_current_user(), variant)}

        except odm.error.EntityNotFound:
            return {'status': False}


class Toggle(routing.Controller):
    """Toggle a flag
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')
        score = float(self.arg('score', 1.0))

        try:
            author = auth.get_current_user()
            entity = odm.get_by_ref(entity)
            count = _api.toggle(entity, author, variant, score)

            return {
                'count': count,
                'status': _api.is_flagged(entity, author, variant),
            }

        except odm.error.EntityNotFound:
            raise self.not_found("Entity '{}' is not found".format(entity))

        except errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class Delete(routing.Controller):
    """Delete a flag
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')

        try:
            return {'count': _api.delete(odm.get_by_ref(entity), auth.get_current_user(), variant)}

        except odm.error.EntityNotFound:
            raise self.not_found("Entity '{}' is not found".format(entity))

        except errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class Count(routing.Controller):
    """Get flags count
    """

    def exec(self) -> dict:
        entity = self.arg('entity')
        variant = self.arg('variant')

        try:
            return {'count': _api.count(odm.get_by_ref(entity), variant)}
        except odm.error.EntityNotFound:
            return {'count': 0}
