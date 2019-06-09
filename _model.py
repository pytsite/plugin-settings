"""PytSite Settings Plugin Data Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins import odm


class Setting(odm.model.Entity):
    def _setup_fields(self):
        """Hook
        """
        self.define_field(odm.field.String('uid', is_required=True))
        self.define_field(odm.field.Dict('value'))

    def _setup_indexes(self):
        """Hook
        """
        self.define_index([('uid', odm.I_ASC)])
