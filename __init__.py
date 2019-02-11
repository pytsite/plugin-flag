"""PytSite Flag Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import semver as _semver

# Public API
from . import _model as model, _widget as widget
from ._api import define, create, count, delete_all, is_flagged, toggle, delete, is_defined, find


def plugin_load():
    from pytsite import events
    from plugins import permissions, odm
    from . import _api, _model, _eh, _http_api_controllers

    # Permission group
    permissions.define_group('flag', 'flag@flag')

    # ODM models
    odm.register_model('flag', _model.Flag)

    # Event listeners
    events.listen('odm@entity.delete', _eh.odm_entity_delete)

    # Define default flag variants
    _api.define('like')
    _api.define('dislike')
    _api.define('bookmark')


def plugin_install():
    from plugins import auth

    # Allow ordinary users to create, modify and delete images
    for role in auth.find_roles():
        role.permissions = list(role.permissions) + [
            'odm_auth@create.flag',
            'odm_auth@delete_own.flag',
        ]
        role.save()


def plugin_load_wsgi():
    from plugins import http_api
    from . import _http_api_controllers

    # HTTP API handlers
    http_api.handle('GET', 'flag/<variant>/<entity>', _http_api_controllers.Status, 'flag@status')
    http_api.handle('GET', 'flag/count/<variant>/<entity>', _http_api_controllers.Count, 'flag@count')
    http_api.handle('POST', 'flag/<variant>/<entity>', _http_api_controllers.Create, 'flag@create')
    http_api.handle('DELETE', 'flag/<variant>/<entity>', _http_api_controllers.Delete, 'flag@delete')
    http_api.handle('PATCH', 'flag/<variant>/<entity>', _http_api_controllers.Toggle, 'flag@toggle')


def plugin_update(v_from: _semver.Version):
    if v_from < '2.3':
        # Type of the field 'entity' was changed from Ref to ManualRef,
        # so it's necessary to re-save all the flags to update this field
        from plugins import odm
        odm.clear_cache('flag')
        for e in odm.find('flag').get():
            e.save(force=True, pre_hooks=False, after_hooks=False, update_timestamp=False)

    elif v_from < '4.0':
        # Model's fieldset changed
        from plugins import odm
        odm.reindex('flag')
