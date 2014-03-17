# -*- coding: utf-8 -*-

'''Opus decoder.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'OpusDecoder',
        ]

from . import base
from . import llinterface
from . import utils


class OpusDecoder(base.OpusCodec):
    '''Opus decoder.'''

    def __init__(self, frequency, channels):
        # basic sanity check
        utils.check_freq(frequency)
        utils.check_channels(channels)

        self.frequency = frequency
        self.channels = channels

        # initialize state
        super(OpusDecoder, self).__init__()

    def _get_state_size(self):
        return llinterface.decoder_get_size(self.channels)

    def _init_state(self):
        llinterface.decoder_init(self._state, self.frequency, self.channels)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
