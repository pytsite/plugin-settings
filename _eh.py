"""PytSite Settings Plugin Event Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang, metatag, router, reg


def on_dispatch():
    settings = reg.get('app')

    # Add meta tags for home page
    if settings and router.is_base_url():
        lng = lang.get_current()
        for s_key in ['title', 'description', 'keywords']:
            s_full_key = 'home_{}_{}'.format(s_key, lng)
            if s_full_key in settings:
                s_val = settings[s_full_key]
                if isinstance(s_val, list):
                    s_val = ','.join(s_val)
                metatag.t_set(s_key, s_val)

                if s_key in ['title', 'description']:
                    metatag.t_set('og:' + s_key, s_val)
                    metatag.t_set('twitter:' + s_key, s_val)
