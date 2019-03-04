"""PytSite Settings Plugin Data Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import odm as _odm


class Setting(_odm.model.Entity):
    def _setup_fields(self):
        """Hook
        """
        self.define_field(_odm.field.String('uid', is_required=True))
        self.define_field(_odm.field.Dict('value'))

    def _setup_indexes(self):
        """Hook
        """
        self.define_index([('uid', _odm.I_ASC)])
