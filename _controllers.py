"""PytSite Settings Plugin Controllers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import metatag, lang, routing, tpl
from plugins import admin as admin
from . import _api, _frm


class GetForm(routing.Controller):
    """Settings Form
    """

    def exec(self) -> str:
        uid = self.arg('uid')

        # Load setting definition
        setting_def = _api.get_definition(uid)

        # Update page's title
        metatag.t_set('title', lang.t(setting_def['title']))

        content = setting_def['content']
        if issubclass(content, _frm.Form):
            return admin.render(tpl.render('settings@form', {'form': content(self.request, setting_uid=uid)}))
        elif callable(content):
            return admin.render(content())
        else:
            return content
