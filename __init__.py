"""PytSite Settings Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import is_defined, define, form_url
from ._frm import Form


def plugin_load():
    from pytsite import reg
    from plugins import odm
    from . import _api, _model, _frm, _driver

    # ODM models
    odm.register_model('setting', _model.Setting)

    # Registry driver
    reg.set_driver(_driver.Registry(reg.get_driver()))


def plugin_load_wsgi():
    from pytsite import router
    from plugins import admin, auth_ui
    from . import _controllers, _eh

    # Routing
    abp = admin.base_path()
    router.handle(_controllers.GetForm, abp + '/settings/<uid>', 'settings@get_form', filters=auth_ui.AuthFilter)

    # Admin sidebar's section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, 'title')

    # Define default application settings form
    define('app', _frm.Application, __name__ + '@application', 'fa fa-cube')

    # Event handlers
    router.on_dispatch(_eh.on_dispatch)
