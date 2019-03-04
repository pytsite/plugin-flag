"""PytSite Flag Plugin ODM Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Tuple as _Tuple
from decimal import Decimal as _Decimal
from plugins import auth as _auth, odm as _odm, auth_storage_odm as _auth_storage_odm, odm_auth as _odm_auth
from . import _api


class Flag(_odm_auth.model.OwnedEntity):
    """Flag ODM Model
    """

    @property
    def variant(self) -> str:
        return self.f_get('variant')

    @property
    def entity(self) -> _odm.model.Entity:
        return self.f_get('entity')

    @property
    def author(self) -> _auth.model.AbstractUser:
        return self.f_get('author')

    @property
    def score(self) -> _Decimal:
        return self.f_get('score')

    def _setup_fields(self):
        """Hook
        """
        self.define_field(_odm.field.String('variant', is_required=True, default='like'))
        self.define_field(_odm.field.Ref('entity', is_required=True))
        self.define_field(_auth_storage_odm.field.User('author', is_required=True))
        self.define_field(_odm.field.Decimal('score', default=1.0))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('variant', _odm.I_ASC), ('entity', _odm.I_ASC), ('author', _odm.I_ASC)], unique=True)

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook
        """
        if field_name == 'variant' and not _api.is_defined(value):
            raise ValueError("Flag variant '{}' is not defined".format(value))

        return super()._on_f_set(field_name, value, **kwargs)

    @classmethod
    def odm_auth_permissions(cls) -> _Tuple[str, ...]:
        return 'create', 'delete_own'
