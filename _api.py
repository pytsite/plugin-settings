"""PytSite Settings Plugin API Functions
"""
from typing import Type as _Type
from pytsite import router as _router
from plugins import admin as _admin
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


def form_url(uid: str) -> str:
    """Get URL of a settings form
    """
    return _router.rule_url('settings@form', {'uid': uid})
