"""PytSite Settings Plugin Forms
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router as _router, lang as _lang, validation as _validation, events as _events, reg as _reg
from plugins import widget as _widget, form as _form


class Form(_form.Form):
    """Base settings form
    """

    def __init__(self, **kwargs):
        """Init
        """
        self._setting_uid = kwargs.get('setting_uid')

        kwargs.update({
            'name': 'settings-' + self._setting_uid,
            'action': _router.rule_url('settings@post_form', {'uid': self._setting_uid}),
            'css': 'settings-form setting-uid-' + self._setting_uid,
        })

        super().__init__(**kwargs)

    def _on_setup_widgets(self):
        """Hook
        """
        _events.fire('settings@form.setup_widgets', frm=self)
        _events.fire('settings@form.setup_widgets.' + self._setting_uid, frm=self)

        # Fill form widgets with values
        for k, v in _reg.get(self._setting_uid, {}).items():
            try:
                self.get_widget('setting_' + k).value = v
            except _form.error.WidgetNotExist:
                pass

        self.add_widget(_widget.button.Link(
            uid='action-cancel-' + str(self.step),
            weight=10,
            value=_lang.t('settings@cancel'),
            icon='fa fa-fw fa-ban',
            href=_router.rule_url('admin@dashboard'),
            form_area='footer',
        ))


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
