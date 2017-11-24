"""PytSite Settings Plugin API Functions
"""
from typing import Any as _Any, Type as _Type
from pytsite import router as _router, reg as _reg
from plugins import admin as _admin, odm as _odm
from . import _frm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_settings = {}


def is_defined(uid: str) -> bool:
    """Check if the setting is already defined.
    """
    return uid in _settings


def define(uid: str, frm: _Type[_frm.Form], menu_title: str, menu_icon: str, permissions: str = '*',
           menu_weight: int = 0):
    """Define a setting
    """
    if uid in _settings:
        raise KeyError("Setting '{}' is already defined.".format(uid))

    _settings[uid] = {
        'title': menu_title,
        'form': frm,
        'perm_name': permissions,
    }

    url = _router.rule_path('settings@form', {'uid': uid})
    _admin.sidebar.add_menu('settings', uid, menu_title, url, menu_icon, weight=menu_weight, permissions=permissions)


def get_definition(uid: str) -> dict:
    """Get setting's definition
    """
    if uid not in _settings:
        raise KeyError("Setting '{}' is not defined.".format(uid))

    return _settings[uid]


def get(uid: str, default: _Any = None) -> _Any:
    """Get setting's value
    """
    uid_split = uid.split('.')

    if uid_split[0] not in _settings:
        raise KeyError("Setting '{}' is not defined.".format(uid_split[0]))

    entity = _odm.find('setting').eq('uid', uid_split[0]).first()
    if not entity:
        if default is not None:
            return default

        return _reg.get(uid, {} if len(uid_split) == 1 else default)

    setting_value = entity.f_get('value')
    if len(uid_split) == 2:
        return setting_value.get(uid_split[1], default)
    else:
        return setting_value


def put(uid: str, value: _Any):
    """Set setting's value
    """
    uid_split = uid.split('.')

    if uid_split[0] not in _settings:
        raise KeyError("Setting '{}' is not defined.".format(uid_split[0]))

    entity = _odm.find('setting').eq('uid', uid_split[0]).first()
    if not entity:
        entity = _odm.dispense('setting').f_set('uid', uid_split[0])

    stored_value = dict(entity.f_get('value'))
    if len(uid_split) == 2:
        stored_value[uid_split[1]] = value
        entity.f_set('value', stored_value)
    else:
        entity.f_set('value', value)

    entity.save()


def form_url(uid: str) -> str:
    """Get URL of a settings form
    """
    return _router.rule_url('settings@form', {'uid': uid})
