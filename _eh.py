"""PytSite Flag Plugin Event Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import odm
from . import _api


def odm_entity_delete(entity: odm.model.Entity):
    """'odm.entity.delete' event handler.
    """
    # Delete all related flags on entity deletion.
    _api.delete_all(entity)
