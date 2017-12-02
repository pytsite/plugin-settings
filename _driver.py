"""PytSite Settings Plugin Registry Driver
"""
from typing import Any as _Any
from pytsite import reg
from plugins import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Registry(reg.driver.Abstract):
    def _get(self, key: str) -> _Any:
        """Get setting's value
        """
        key = key.split('.')
        key_split_len = len(key)

        if key_split_len > 2:
            raise RuntimeError('No more than one dot is currently supported by this registry driver: {}'.format(key))

        entity = _odm.find('setting').eq('uid', key[0]).first()
        if not entity:
            return

        setting_value = dict(entity.f_get('value'))

        return setting_value[key[1]] if key_split_len == 2 else setting_value

    def _put(self, key: str, value: _Any):
        """Set setting's value
        """
        key_split = key.split('.')
        key_split_len = len(key_split)

        if key_split_len > 2:
            raise RuntimeError('No more than one dot is currently supported by this registry driver: {}'.format(key))

        entity = _odm.find('setting').eq('uid', key_split[0]).first()
        if not entity:
            entity = _odm.dispense('setting').f_set('uid', key_split[0])

        if key_split_len == 2:
            stored_value = dict(entity.f_get('value'))
            stored_value[key_split[1]] = value
            entity.f_set('value', stored_value)
        else:
            entity.f_set('value', value)

        entity.save()
