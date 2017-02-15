"""Flag Package Models.
"""
from typing import Tuple as _Tuple
from pytsite import odm as _odm, auth_storage_odm as _auth_storage_odm, odm_auth as _odm_auth
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Flag(_odm_auth.model.AuthorizableEntity):
    """Flag ODM Model.
    """

    @classmethod
    def odm_auth_permissions(cls) -> _Tuple[str]:
        return 'create', 'delete_own'

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('type', default='like'))
        self.define_field(_odm.field.Ref('entity', required=True))
        self.define_field(_auth_storage_odm.field.User('author', required=True))
        self.define_field(_odm.field.Decimal('score', default=1.0))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('entity', _odm.I_ASC), ('author', _odm.I_ASC)], unique=True)
        self.define_index([('entity', _odm.I_ASC), ('type', _odm.I_ASC)])

    def _on_f_set(self, field_name: str, value, **kwargs):
        if field_name == 'type' and not _api.is_defined(value):
            raise ValueError("Flag type '{}' is not defined".format(value))

        return super()._on_f_set(field_name, value, **kwargs)
