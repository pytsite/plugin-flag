"""PytSite Flag Package.
"""
# Public API
from . import _widget as widget
from ._api import define, create, average, count, delete_all, is_flagged, total, toggle, delete

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, odm, tpl, lang, events, http_api, permissions
    from . import _model, _eh, _http_api_controllers

    # Resources
    lang.register_package(__name__, alias='flag')
    tpl.register_package(__name__, alias='flag')

    assetman.register_package(__name__, alias='flag')
    assetman.js_module('flag-widget-like', __name__ + '@js/flag-widget-like')
    assetman.t_less(__name__ + '@css/**', 'css')
    assetman.t_js(__name__ + '@js/**', 'js')

    # Permission group
    permissions.define_group('flag', 'flag@flag')

    # ODM models
    odm.register_model('flag', _model.Flag)

    # HTTP API handlers
    http_api.handle('POST', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Post(), 'flag@post')
    http_api.handle('GET', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Get(), 'flag@get')
    http_api.handle('PATCH', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Patch(), 'flag@patch')
    http_api.handle('DELETE', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Delete(), 'flag@delete')
    http_api.handle('GET', 'flag/count/<flag_type>/<model>/<uid>', _http_api_controllers.GetCount(), 'flag@get_count')

    # Event listeners
    events.listen('pytsite.setup', _eh.setup)
    events.listen('pytsite.odm.entity.delete', _eh.odm_entity_delete)

    # Define default flag types
    define('like')
    define('bookmark')


_init()
