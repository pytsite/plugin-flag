"""PytSite Flag Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union as _Union, Optional as _Optional
from pytsite import html as _html
from plugins import widget as _widget, odm as _odm, auth as _auth
from . import _api


class Flag(_widget.Abstract):
    def __init__(self, uid: str, variant: str, entity: _Union[str, _odm.Entity], **kwargs):
        """Init
        """
        super().__init__(uid, has_messages=False, **kwargs)

        self._variant = variant
        self._entity = entity
        self._icon = kwargs.get('icon', 'fas fa-thumbs-up')
        self._counter_format = kwargs.get('counter_format', '#')
        self._link = kwargs.get('link', '')
        self._link_target = kwargs.get('link_target', '_self')
        self._link_data_toggle = kwargs.get('link_data_toggle')
        self._link_data_target = kwargs.get('link_data_target')

        if not _api.is_defined(self._variant):
            raise ValueError("Flag variant '{}' is not defined".format(self._variant))

    def _get_element(self, **kwargs) -> _Optional[_html.Element]:
        """Hook
        """
        if not _auth.get_current_user().is_authenticated:
            return None

        self._data.update({
            'count': _api.count(self._entity),
            'counter_format': self._counter_format,
            'css': self._css,
            'entity': self._entity,
            'icon': self._icon,
            'is_flagged': _api.is_flagged(self._entity),
            'link': self._link,
            'link_data_target': self._link_data_target,
            'link_data_toggle': self._link_data_toggle,
            'link_target': self._link_target,
            'variant': self._variant,
        })

        return _html.Div(css='widget-component')
