"""PytSite Settings Plugin
"""
# Public API
from ._api import is_defined, define, form_url
from ._frm import Form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import reg, lang, router
    from plugins import permissions, odm, admin
    from . import _api, _model, _controllers, _frm, _eh, _driver

    # Resources
    lang.register_package(__name__)

    # ODM model
    odm.register_model('setting', _model.Setting)

    # Registry driver
    reg.set_driver(_driver.Registry(reg.get_driver()))

    # Routing
    router.handle(_controllers.Form, admin.base_path() + '/settings/<uid>', 'settings@form',
                  filters=admin.AdminAccessFilterController)

    # Admin sidebar section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, sort_items_by='title')

    # Define default application settings form
    permissions.define_permission('app.settings.manage', __name__ + '@manage_app_settings', 'app')
    define('app', _frm.Application, __name__ + '@application', 'fa fa-cube', 'app.settings.manage')

    # Event handlers
    router.on_dispatch(_eh.on_dispatch)


_init()
