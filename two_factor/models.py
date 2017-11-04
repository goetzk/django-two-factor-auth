from __future__ import absolute_import, division, unicode_literals

from django.utils.translation import ugettext_lazy as _
from django_otp.util import hex_validator

import logging
logger = logging.getLogger(__name__)


def get_available_methods():
    methods = []
    # FIXME:
    # for each registered backend
    #   methods.extend(backend.name.get_available_methods())
    return methods


def key_validator(*args, **kwargs):
    """Wraps hex_validator generator, to keep makemigrations happy."""
    return hex_validator()(*args, **kwargs)


