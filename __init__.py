"""PytSite Settings Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import is_defined, define, form_url
from ._frm import Form


def plugin_load():
    from pytsite import reg, lang
    from plugins import odm
    from . import _api, _model, _frm, _driver

    # Resources
    lang.register_package(__name__)

    # ODM models
    odm.register_model('setting', _model.Setting)

    # Registry driver
    reg.set_driver(_driver.Registry(reg.get_driver()))


def plugin_load_uwsgi():
    from pytsite import router, tpl
    from plugins import admin, auth_ui
    from . import _controllers, _eh

    tpl.register_package(__name__)

    # Routing
    abp = admin.base_path()
    router.handle(_controllers.GetForm, abp + '/settings/<uid>', 'settings@get_form',
                  filters=auth_ui.AuthFilterController)
    router.handle(_controllers.PostForm, abp + '/settings/<uid>', 'settings@post_form', methods='POST',
                  filters=auth_ui.AuthFilterController)

    # Admin sidebar's section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, 'title')

    # Define default application settings form
    define('app', _frm.Application, __name__ + '@application', 'fa fa-cube')

    # Event handlers
    router.on_dispatch(_eh.on_dispatch)
