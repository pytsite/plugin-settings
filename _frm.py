"""PytSite Settings Plugin Forms
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from pytsite import router as _router, lang as _lang, validation as _validation, events as _events, reg as _reg, \
    util as _util, http as _http
from plugins import widget as _widget, form as _form


class Form(_form.Form):
    """Base settings form
    """

    def _on_setup_form(self):
        setting_uid = self.attr('setting_uid')
        if not setting_uid:
            raise ValueError('setting_uid is not defined')

        self.name = 'settings_' + setting_uid
        self.css = 'settings-form setting-uid-' + setting_uid

    def _on_setup_widgets(self):
        """Hook
        """
        setting_uid = self.attr('setting_uid')

        _events.fire('settings@form.setup_widgets', frm=self)
        _events.fire('settings@form.setup_widgets.' + setting_uid, frm=self)

        # Fill form widgets with values
        for k, v in _reg.get(setting_uid, {}).items():
            try:
                self.get_widget('setting_' + k).value = v
            except _form.WidgetNotExistError:
                pass

        # "Cancel" button
        self.add_widget(_widget.button.Link(
            uid='action_cancel-' + str(self.current_step),
            weight=100,
            value=_lang.t('settings@cancel'),
            icon='fa fas fa-fw fa-ban',
            href=_router.rule_url('admin@dashboard'),
            form_area='footer',
        ))

    def _on_submit(self):
        setting_uid = self.attr('setting_uid')

        # Extract all values who's name starts with 'setting_'
        setting_value = _reg.get(setting_uid, {})
        for k, v in self.values.items():
            if k.startswith('setting_'):
                k = _re.sub('^setting_', '', k)

                if isinstance(v, (list, tuple)):
                    v = _util.cleanup_list(v)

                if isinstance(v, dict):
                    v = _util.cleanup_dict(v)

                setting_value[k] = v

        # Update settings
        _reg.put(setting_uid, setting_value)

        # Notify user
        _router.session().add_success_message(_lang.t('settings@settings_has_been_saved'))

        return _http.RedirectResponse(_router.rule_url('settings@get_form', {'uid': setting_uid}))


class Application(Form):
    """Basic application's settings form
    """

    def _on_setup_widgets(self):
        """Hook
        """
        # Application names
        w = 10
        for l in _lang.langs():
            self.add_widget(_widget.input.Text(
                uid='setting_app_name_' + l,
                weight=w,
                label=_lang.t('settings@application_name', {'lang': _lang.lang_title(l)}, l),
                default=_lang.t('app_name'),
            ))
            w += 1

            self.add_widget(_widget.input.Text(
                uid='setting_home_title_' + l,
                label=_lang.t('settings@home_page_title', {'lang': _lang.lang_title(l)}, l),
                weight=w,
            ))
            w += 1

            self.add_widget(_widget.input.Text(
                uid='setting_home_description_' + l,
                label=_lang.t('settings@home_page_description', {'lang': _lang.lang_title(l)}, l),
                weight=w,
            ))
            w += 1

            self.add_widget(_widget.input.Tokens(
                uid='setting_home_keywords_' + l,
                label=_lang.t('settings@home_page_keywords', {'lang': _lang.lang_title(l)}, l),
                weight=w,
            ))
            w += 1

        # Links
        self.add_widget(_widget.input.StringList(
            uid='setting_links',
            weight=200,
            label=_lang.t('settings@links'),
            add_btn_label=_lang.t('settings@add_link'),
            unique=True,
            rules=_validation.rule.Url(),
        ))

        # It is important to call super method AFTER
        super()._on_setup_widgets()
