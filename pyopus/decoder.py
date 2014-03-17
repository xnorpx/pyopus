# -*- coding: utf-8 -*-

'''Opus decoder.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'OpusDecoder',
        ]

from . import base
from . import llinterface
from . import ctl
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

    def reset_state(self):
        ctl.decoder_reset_state(self._state)

    @property
    def final_range(self):
        return ctl.decoder_get_final_range(self._state)

    @property
    def pitch(self):
        return ctl.decoder_get_pitch(self._state)

    @property
    def bandwidth(self):
        return ctl.decoder_get_bandwidth(self._state)

    @property
    def gain(self):
        return ctl.decoder_get_gain(self._state)

    @gain.setter
    def gain(self, value):
        ctl.decoder_set_gain(self._state, value)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
