"""PytSite Flag Plugin Event Handlers
"""
from plugins import auth as _auth, odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def setup():
    """`pytsite.setup` event handler.
    """
    _auth.switch_user_to_system()

    # Allow ordinary users to create, modify and delete images
    for role in _auth.get_roles():
        role.permissions = list(role.permissions) + [
            'odm_auth.create.flag',
            'odm_auth.delete_own.flag',
        ]
        role.save()

    _auth.restore_user()


def odm_entity_delete(entity: _odm.model.Entity):
    """'odm.entity.delete' event handler.
    """
    # Delete all related flags on entity deletion.
    _api.delete_all(entity)
