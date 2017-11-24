"""PytSite Settings Plugin
"""
# Public API
from ._api import is_defined, define, get, put, form_url
from ._frm import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import tpl, lang, router, package_info
    from plugins import permissions, odm, admin
    from . import _api, _model, _controllers, _frm, _eh

    # Resources
    lang.register_package(__name__)
    tpl.register_global('settings_get', _api.get)

    # Lang globals
    lang.register_global('app_name', lambda language, args: get('app.app_name_' + language, 'PytSite'))
    lang.register_global('app@app_name', lambda language, args: get('app.app_name_' + language, 'PytSite'))

    # Tpl globals
    tpl.register_global('app_name', lambda: get('app.app_name_' + lang.get_current(), 'PytSite'))
    tpl.register_global('app_version', package_info.version('app'))

    # ODM model
    odm.register_model('setting', _model.Setting)

    # Routing
    router.handle(_controllers.Form(), admin.base_path() + '/settings/<uid>', 'settings@form')

    # Admin sidebar section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, sort_items_by='title')

    # Define default application settings form
    permissions.define_permission('app.settings.manage', __name__ + '@manage_app_settings', 'app')
    define('app', _frm.Application, __name__ + '@application', 'fa fa-cube', 'app.settings.manage')

    # Event handlers
    router.on_dispatch(_eh.on_dispatch)


_init()
