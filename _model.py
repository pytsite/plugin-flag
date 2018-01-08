"""PytSite Flag Plugin Models
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Tuple as _Tuple
from decimal import Decimal as _Decimal
from plugins import auth as _auth, odm as _odm, auth_storage_odm as _auth_storage_odm, odm_auth as _odm_auth
from . import _api


class Flag(_odm_auth.model.OwnedEntity):
    """Flag ODM Model.
    """

    @classmethod
    def odm_auth_permissions(cls) -> _Tuple[str, ...]:
        return 'create', 'delete_own'

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('type', default='like'))
        self.define_field(_odm.field.Ref('entity', required=True))
        self.define_field(_auth_storage_odm.field.User('author', required=True))
        self.define_field(_odm.field.Decimal('score', default=1.0))

    @property
    def type(self) -> str:
        return self.f_get('type')

    @property
    def entity(self) -> _odm.model.Entity:
        return self.f_get('entity')

    @property
    def author(self) -> _auth.model.AbstractUser:
        return self.f_get('author')

    @property
    def score(self) -> _Decimal:
        return self.f_get('score')

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('entity', _odm.I_ASC), ('type', _odm.I_ASC), ('author', _odm.I_ASC)], unique=True)

    def _on_f_set(self, field_name: str, value, **kwargs):
        if field_name == 'type' and not _api.is_defined(value):
            raise ValueError("Flag type '{}' is not defined".format(value))

        return super()._on_f_set(field_name, value, **kwargs)
