"""PytSite Settings Plugin Event Handlers
"""
from pytsite import lang as _lang, metatag as _metatag, router as _router
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def on_dispatch():
    settings = _api.get('app')

    # Add meta tags for home page
    if _router.is_base_url():
        lng = _lang.get_current()
        for s_key in ['title', 'description', 'keywords']:
            s_full_key = 'home_{}_{}'.format(s_key, lng)
            if s_full_key in settings:
                s_val = settings[s_full_key]
                if isinstance(s_val, list):
                    s_val = ','.join(s_val)
                _metatag.t_set(s_key, s_val)

                if s_key in ['title', 'description']:
                    _metatag.t_set('og:' + s_key, s_val)
                    _metatag.t_set('twitter:' + s_key, s_val)
