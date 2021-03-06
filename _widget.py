"""PytSite Flag Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import Union, Optional
from pytsite import lang
from plugins import widget, odm, auth, auth_ui
from . import _api


class Flag(widget.Abstract):
    def __init__(self, uid: str, variant: str, entity: Union[str, odm.Entity], **kwargs):
        """Init
        """
        super().__init__(uid, has_messages=False, form_group=False, **kwargs)

        self._variant = variant
        self._entity = entity
        self._flagged_caption = kwargs.get('flagged_caption')
        self._flagged_icon = kwargs.get('flagged_icon')
        self._unflagged_caption = kwargs.get('unflagged_caption')
        self._unflagged_icon = kwargs.get('unflagged_icon')
        self._counter_format = kwargs.get('counter_format', '(#)')
        self._btn_css = kwargs.get('btn_css', 'btn btn-link')
        self._link = kwargs.get('link', '')
        self._link_target = kwargs.get('link_target', '_self')
        self._link_data_toggle = kwargs.get('link_data_toggle')
        self._link_data_target = kwargs.get('link_data_target')

        if not auth.get_current_user().is_authenticated and not self._link:
            self._link = auth_ui.sign_in_url()

    def _get_element(self, **kwargs) -> Optional[htmler.Element]:
        """Hook
        """
        self._data.update({
            'count': _api.count(self._entity, self._variant),
            'counter_format': self._counter_format,
            'css': self._btn_css,
            'entity': self._entity,
            'flagged_caption': self._flagged_caption,
            'flagged_icon': self._flagged_icon,
            'icon': self._flagged_icon,
            'is_flagged': _api.is_flagged(self._entity, auth.get_current_user(), self._variant),
            'link': self._link,
            'link_data_target': self._link_data_target,
            'link_data_toggle': self._link_data_toggle,
            'link_target': self._link_target,
            'title': self._title,
            'unflagged_caption': self._unflagged_caption,
            'unflagged_icon': self._unflagged_icon,
            'variant': self._variant,
        })

        return htmler.Div(css='widget-component')


class Like(Flag):
    def __init__(self, uid: str, entity: Union[str, odm.Entity], **kwargs):
        """Init
        """
        kwargs.setdefault('unflagged_icon', 'far fa-fw fa-thumbs-up')
        kwargs.setdefault('unflagged_caption', lang.t('flag@add_to_liked'))
        kwargs.setdefault('flagged_icon', 'fas fa-fw fa-thumbs-up')
        kwargs.setdefault('flagged_caption', lang.t('flag@remove_from_liked'))

        super().__init__(uid, 'like', entity, **kwargs)


class Bookmark(Flag):
    def __init__(self, uid: str, entity: Union[str, odm.Entity], **kwargs):
        """Init
        """
        kwargs.setdefault('unflagged_icon', 'far fa-fw fa-bookmark')
        kwargs.setdefault('unflagged_caption', lang.t('flag@add_to_bookmarks'))
        kwargs.setdefault('flagged_icon', 'fas fa-fw fa-bookmark')
        kwargs.setdefault('flagged_caption', lang.t('flag@remove_from_bookmarks'))

        super().__init__(uid, 'bookmark', entity, **kwargs)
