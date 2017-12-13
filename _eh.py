"""PytSite Flag Plugin Event Handlers
"""
from plugins import odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def odm_entity_delete(entity: _odm.model.Entity):
    """'odm.entity.delete' event handler.
    """
    # Delete all related flags on entity deletion.
    _api.delete_all(entity)
