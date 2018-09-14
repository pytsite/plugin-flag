"""PytSite Flag Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import semver as _semver

# Public API
from . import _model as model
from ._api import define, create, average, count, delete_all, is_flagged, total, toggle, delete, is_defined, find


def plugin_load():
    from pytsite import lang, events
    from plugins import permissions, odm
    from . import _api, _model, _eh, _http_api_controllers

    # Resources
    lang.register_package(__name__)

    # Permission group
    permissions.define_group('flag', 'flag@flag')

    # ODM models
    odm.register_model('flag', _model.Flag)

    # Event listeners
    events.listen('odm@entity.delete', _eh.odm_entity_delete)

    # Define default flag types
    _api.define('like')
    _api.define('bookmark')


def plugin_install():
    from plugins import auth, assetman

    # Allow ordinary users to create, modify and delete images
    for role in auth.find_roles():
        role.permissions = list(role.permissions) + [
            'odm_auth@create.flag',
            'odm_auth@delete_own.flag',
        ]
        role.save()

    assetman.build(__name__)
    assetman.build_translations()


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
        from plugins import odm

        # Type of the field 'entity' was changed from Ref to ManualRef,
        # so it's necessary to re-save all the flags to update this field
        odm.clear_cache('flag')
        for e in odm.find('flag').get():
            e.save(force=True, pre_hooks=False, after_hooks=False, update_timestamp=False)
