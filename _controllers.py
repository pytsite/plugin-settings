"""PytSite Settings Plugin Controllers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from pytsite import metatag as _metatag, lang as _lang, routing as _routing, tpl as _tpl, util as _util, reg as _reg, \
    router as _router
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

        content = setting_def['content'](setting_uid=uid)
        if isinstance(content, _frm.Form):
            return _admin.render(_tpl.render('settings@form', {'form': content}))
        else:
            return _admin.render(content)


class PostForm(_routing.Controller):
    """Settings Form Submit
    """

    def exec(self):
        setting_uid = self.arg('uid')

        # Extract all values who's name starts with 'setting_'
        setting_value = {}
        for k, v in self.request.inp.items():
            if k.startswith('setting_'):
                k = _re.sub('^setting_', '', k)

                if isinstance(v, (list, tuple)):
                    v = _util.cleanup_list(v)

                if isinstance(v, dict):
                    v = _util.cleanup_dict(v)

                setting_value[k] = v

        # Update settings
        _reg.put(setting_uid, _util.dict_merge(_reg.get(setting_uid, {}), setting_value))

        _router.session().add_success_message(_lang.t('settings@settings_has_been_saved'))

        return self.redirect(_router.rule_url('settings@get_form', {'uid': setting_uid}))
