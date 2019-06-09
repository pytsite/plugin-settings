"""PytSite Settings Plugin API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Type, Union
from pytsite import router
from plugins import admin
from . import _frm

_settings = {}


def is_defined(uid: str) -> bool:
    """Check if the setting is already defined.
    """
    return uid in _settings


def define(uid: str, content: Type[_frm.Form], title: str, icon: str,
           roles: Union[str, list, tuple] = ('admin', 'dev'), permissions: Union[str, list, tuple] = None,
           weight: int = 0):
    """Define a setting
    """
    if uid in _settings:
        raise KeyError("Setting '{}' is already defined".format(uid))

    _settings[uid] = {
        'title': title,
        'content': content,
    }

    path = router.rule_path('settings@get_form', {'uid': uid})
    admin.sidebar.add_menu('settings', uid, title, path, icon, weight=weight, roles=roles, permissions=permissions)


def get_definition(uid: str) -> dict:
    """Get setting's definition
    """
    if uid not in _settings:
        raise KeyError("Setting '{}' is not defined".format(uid))

    return _settings[uid]


def form_url(uid: str) -> str:
    """Get URL of a settings form
    """
    return router.rule_url('settings@get_form', {'uid': uid})
