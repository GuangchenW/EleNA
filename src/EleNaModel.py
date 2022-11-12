import os
from urllib.request import urlopen, Request
import re
import base64
import mimetypes

from flexx import flx

_leaflet_url = 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/'
_leaflet_version = '1.0.3'
_leaflet_icons = [
    'marker-icon.png',
    'marker-icon-2x.png',
    'marker-shadow.png',
]


if 'LEAFLET_DIR' in os.environ:
    _base_url = 'file://%s' % os.environ['LEAFLET_DIR']
else:
    _base_url = '%s/%s' % (_leaflet_url, _leaflet_version)
mimetypes.init()


def _get_code(item):
    """ Get a text item from _base_url
    """
    url = '%s/%s' % (_base_url, item)
    req = Request(url, headers={'User-Agent': 'flexx/%s' % flx.__version__})
    return urlopen(req).read().decode()


def _get_data(item_or_url):
    """ Get a binary item from url or _base_url
    """
    if '://' in item_or_url:
        url = item_or_url
    else:
        url = '%s/%s' % (_base_url, item_or_url)
    req = Request(url, headers={'User-Agent': 'flexx/%s' % flx.__version__})
    return urlopen(req).read()


def _embed_css_resources(css, types=('.png',)):
    """ Replace urls in css with data urls
    """
    type_str = '|'.join('\%s' % t for t in types)
    rx = re.compile('(url\s*\(\s*(.*(%s))\s*\))' % type_str)
    found = rx.findall(css)
    for match, item, ext in found:
        data = base64.b64encode(_get_data(item)).decode()
        mime = mimetypes.types_map[ext]
        repl = 'url(data:%s;base64,%s)' % (mime, data)
        css = css.replace(match, repl)
    return css


flx.assets.associate_asset(
    __name__,
    'leaflet.js',
    lambda: _get_code('leaflet.js'),
)
flx.assets.associate_asset(
    __name__,
    'leaflet.css',
    lambda: _embed_css_resources(_get_code('leaflet.css')),
)
for icon in _leaflet_icons:
    flx.assets.add_shared_data(icon, _get_data('images/%s' % icon))
