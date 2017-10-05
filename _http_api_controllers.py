"""Pytsite Flag Plugin HTTP API Controllers
"""
from pytsite import auth as _auth, odm as _odm, routing as _routing, errors as _errors
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Post(_routing.Controller):
    """Create a flag
    """

    def exec(self) -> dict:
        model = self.arg('model')
        uid = self.arg('uid')
        flag_type = self.arg('flag_type')
        score = float(self.arg('score', 1.0))

        try:
            return {'count': _api.create(_odm.dispense(model, uid), _auth.get_current_user(), flag_type, score)}

        except _odm.error.EntityNotFound:
            raise self.not_found("Entity '{}:{}' is not found".format(model, uid))

        except _errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class Get(_routing.Controller):
    """Get flag's status
    """

    def exec(self) -> dict:
        model = self.arg('model')
        uid = self.arg('uid')
        flag_type = self.arg('flag_type')

        try:
            return {'status': _api.is_flagged(_odm.dispense(model, uid), _auth.get_current_user(), flag_type)}
        except _odm.error.EntityNotFound:
            return {'status': False}


class Patch(_routing.Controller):
    """Toggle a flag
    """

    def exec(self) -> dict:
        model = self.arg('model')
        uid = self.arg('uid')
        flag_type = self.arg('flag_type')
        score = float(self.arg('score', 1.0))

        try:
            author = _auth.get_current_user()
            entity = _odm.dispense(model, uid)
            count = _api.toggle(entity, author, flag_type, score)

            return {
                'count': count,
                'status': _api.is_flagged(entity, author, flag_type),
            }

        except _odm.error.EntityNotFound:
            raise self.not_found("Entity '{}:{}' is not found".format(model, uid))

        except _errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class Delete(_routing.Controller):
    """Delete a flag
    """

    def exec(self) -> dict:
        model = self.arg('model')
        uid = self.arg('uid')
        flag_type = self.arg('flag_type')

        try:
            return {'count': _api.delete(_odm.dispense(model, uid), _auth.get_current_user(), flag_type)}

        except _odm.error.EntityNotFound:
            raise self.not_found("Entity '{}:{}' is not found".format(model, uid))

        except _errors.ForbidOperation as e:
            raise self.forbidden(str(e))


class GetCount(_routing.Controller):
    """Get flags count
    """

    def exec(self) -> dict:
        model = self.arg('model')
        uid = self.arg('uid')
        flag_type = self.arg('flag_type')

        try:
            return {'count': _api.count(_odm.dispense(model, uid), flag_type)}
        except _odm.error.EntityNotFound:
            return {'count': 0}
