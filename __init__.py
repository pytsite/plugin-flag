"""PytSite Flag Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    # Public API
    from . import _widget as widget
    from ._api import define, create, average, count, delete_all, is_flagged, total, toggle, delete, is_defined, find


def plugin_install():
    from plugins import auth

    auth.switch_user_to_system()

    # Allow ordinary users to create, modify and delete images
    for role in auth.get_roles():
        role.permissions = list(role.permissions) + [
            'odm_auth.create.flag',
            'odm_auth.delete_own.flag',
        ]
        role.save()

    auth.restore_user()


def plugin_load():
    from pytsite import tpl, lang, events
    from plugins import permissions, odm, assetman, http_api
    from . import _model, _eh, _http_api_controllers

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.register_package(__name__)
    assetman.js_module('flag-widget-like', __name__ + '@js/flag-widget-like')
    assetman.t_less(__name__)
    assetman.t_js(__name__)

    # Permission group
    permissions.define_group('flag', 'flag@flag')

    # ODM models
    odm.register_model('flag', _model.Flag)

    # HTTP API handlers
    http_api.handle('GET', 'flag/count/<flag_type>/<model>/<uid>', _http_api_controllers.GetCount, 'flag@get_count')
    http_api.handle('POST', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Post, 'flag@post')
    http_api.handle('GET', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Get, 'flag@get')
    http_api.handle('PATCH', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Patch, 'flag@patch')
    http_api.handle('DELETE', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Delete, 'flag@delete')

    # Event listeners
    events.listen('odm@entity.delete', _eh.odm_entity_delete)

    # Define default flag types
    define('like')
    define('bookmark')
