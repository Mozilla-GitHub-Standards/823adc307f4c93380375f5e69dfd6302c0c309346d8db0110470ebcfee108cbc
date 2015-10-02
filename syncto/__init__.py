import pkg_resources

import cliquet
from pyramid.config import Configurator

# Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__).version

try:
    # Verify that we are using the Py2 urllib3 version with OpenSSL installed
    from requests.packages.urllib3.contrib import pyopenssl
except ImportError:  # Pragma: no cover
    pass
else:
    pyopenssl.inject_into_urllib3()  # Pragma: no cover

AUTHORIZATION_HEADER = 'Authorization'
CLIENT_STATE_HEADER = 'X-Client-State'

DEFAULT_SETTINGS = {
    'syncto.cache_hmac_secret': None,
    'syncto.cache_credentials_ttl_seconds': 300,
    'syncto.record_meta_put_enabled': False,
    'syncto.record_meta_delete_enabled': False,
    'syncto.record_crypto_put_enabled': False,
    'syncto.record_crypto_delete_enabled': False,
}


def main(global_config, **settings):
    config = Configurator(settings=settings)

    if 'syncto.cache_hmac_secret' not in settings:
        raise ValueError(
            "Please configure the `syncto.cache_hmac_secret` settings.")

    cliquet.initialize(config, __version__, default_settings=DEFAULT_SETTINGS)
    config.scan("syncto.views")
    return config.make_wsgi_app()
