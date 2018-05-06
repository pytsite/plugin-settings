"""PytSite Settings Plugin Controllers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import metatag as _metatag, lang as _lang, routing as _routing, tpl as _tpl
from plugins import admin as _admin
from . import _api, _frm


class GetForm(_routing.Controller):
    """Settings Form
    """

    def exec(self) -> str:
        uid = self.arg('uid')

        # Load setting definition
        setting_def = _api.get_definition(uid)

        # Update page's title
        _metatag.t_set('title', _lang.t(setting_def['title']))

        content = setting_def['content']
        if issubclass(content, _frm.Form):
            return _admin.render(_tpl.render('settings@form', {'form': content(self.request, setting_uid=uid)}))
        elif callable(content):
            return _admin.render(content())
        else:
            return content
