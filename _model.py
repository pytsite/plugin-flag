"""PytSite Flag Plugin ODM Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List
from decimal import Decimal
from plugins import auth, odm, auth_storage_odm, odm_auth
from plugins.odm_auth import PERM_CREATE, PERM_DELETE_OWN
from . import _api


class Flag(odm_auth.OwnedEntity):
    """Flag ODM Model
    """

    @property
    def variant(self) -> str:
        return self.f_get('variant')

    @property
    def entity(self) -> odm.model.Entity:
        return self.f_get('entity')

    @property
    def author(self) -> auth.model.AbstractUser:
        return self.f_get('author')

    @property
    def score(self) -> Decimal:
        return self.f_get('score')

    def _setup_fields(self):
        """Hook
        """
        self.define_field(odm.field.String('variant', is_required=True, default='like'))
        self.define_field(odm.field.Ref('entity', is_required=True))
        self.define_field(auth_storage_odm.field.User('author', is_required=True))
        self.define_field(odm.field.Decimal('score', default=1.0))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('variant', odm.I_ASC), ('entity', odm.I_ASC), ('author', odm.I_ASC)], unique=True)

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook
        """
        if field_name == 'variant' and not _api.is_defined(value):
            raise ValueError("Flag variant '{}' is not defined".format(value))

        return super()._on_f_set(field_name, value, **kwargs)

    def odm_auth_permissions(self) -> List[str]:
        return [PERM_CREATE, PERM_DELETE_OWN]
