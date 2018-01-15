"""PytSite Flag Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman, semver as _semver

if _plugman.is_installed(__name__):
    # Public API
    from . import _widget as widget, _model as model
    from ._api import define, create, average, count, delete_all, is_flagged, total, toggle, delete, is_defined, find


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.js_module('flag-widget-like', __name__ + '@js/flag-widget-like')
        assetman.t_less(__name__)
        assetman.t_js(__name__)

    return assetman


def plugin_install():
    from plugins import auth

    # Allow ordinary users to create, modify and delete images
    auth.switch_user_to_system()
    for role in auth.get_roles():
        role.permissions = list(role.permissions) + [
            'odm_auth.create.flag',
            'odm_auth.delete_own.flag',
        ]
        role.save()
    auth.restore_user()

    assetman = _register_assetman_resources()
    assetman.build(__name__)
    assetman.build_translations()


def plugin_load():
    from pytsite import tpl, lang, events
    from plugins import permissions, odm
    from . import _api, _model, _eh, _http_api_controllers

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    _register_assetman_resources()

    # Permission group
    permissions.define_group('flag', 'flag@flag')

    # ODM models
    odm.register_model('flag', _model.Flag)

    # Event listeners
    events.listen('odm@entity.delete', _eh.odm_entity_delete)

    # Define default flag types
    _api.define('like')
    _api.define('bookmark')


def plugin_load_uwsgi():
    from plugins import http_api
    from . import _http_api_controllers

    # HTTP API handlers
    http_api.handle('GET', 'flag/count/<flag_type>/<model>/<uid>', _http_api_controllers.GetCount, 'flag@get_count')
    http_api.handle('POST', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Post, 'flag@post')
    http_api.handle('GET', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Get, 'flag@get')
    http_api.handle('PATCH', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Patch, 'flag@patch')
    http_api.handle('DELETE', 'flag/<flag_type>/<model>/<uid>', _http_api_controllers.Delete, 'flag@delete')


def plugin_update(v_from: _semver.Version):
    if v_from < _semver.Version('2.3'):
        from pytsite import on_app_load

        def update_from_2_3():
            from plugins import odm

            # Type of the field 'entity' was changed from Ref to ManualRef,
            # so it's necessary to re-save all the flags to update this field
            odm.clear_finder_cache('flag')
            for e in odm.find('flag').get():
                e.save(force=True, pre_hooks=False, after_hooks=False, update_timestamp=False)

        on_app_load(update_from_2_3)
