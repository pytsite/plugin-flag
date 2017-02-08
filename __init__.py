"""PytSite Flag Package.
"""
# Public API
from . import _widget as widget
from ._api import flag, average, count, delete, is_flagged, sum, toggle, unflag

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, odm, tpl, lang, events, http_api, permissions
    from . import _model, _eh, _http_api

    # Resources
    lang.register_package(__name__, alias='flag')
    tpl.register_package(__name__, alias='flag')
    assetman.register_package(__name__, alias='flag')

    # Permission group
    permissions.define_group('flag', 'flag@flag')

    # ODM models
    odm.register_model('flag', _model.Flag)

    # HTTP API aliases
    http_api.handle('PATCH', 'flag/toggle/<model>/<uid>', _http_api.patch_toggle, 'flag@toggle')

    # Event listeners
    events.listen('pytsite.setup', _eh.setup)
    events.listen('pytsite.odm.entity.delete', _eh.odm_entity_delete)


_init()
