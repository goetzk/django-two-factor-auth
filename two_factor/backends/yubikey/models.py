from __future__ import absolute_import, division, unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import logging
logger = logging.getLogger(__name__)

try:
    import yubiotp
except ImportError:
    yubiotp = None


def get_available_methods():
    methods = []
    if yubiotp and 'otp_yubikey' in settings.INSTALLED_APPS:
        methods.append(('yubikey', _('YubiKey')))
    return methods


