# -*- coding: utf-8 -*-

'''Opus encoder.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'OpusEncoder',
        ]

from . import binding
from . import llinterface
from . import base
from . import utils


class OpusEncoder(base.OpusCodec):
    '''Opus encoder.'''

    def __init__(self, frequency, channels, application):
        # basic sanity check
        utils.check_freq(frequency)
        utils.check_channels(channels)
        utils.check_application(application)

        self.frequency = frequency
        self.channels = channels
        self.application = application

        # initialize state
        super(OpusEncoder, self).__init__()

    def _get_state_size(self):
        return llinterface.encoder_get_size(self.channels)

    def _init_state(self):
        llinterface.encoder_init(
                self._state,
                self.frequency,
                self.channels,
                self.application,
                )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
