# -*- coding: utf-8 -*-

'''Opus encoder.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'OpusEncoder',
        ]

from . import base
from . import llinterface
from . import ctl
from . import utils


class OpusEncoder(base.OpusCodec):
    '''Opus encoder.'''

    def __init__(self, frequency, channels, application):
        # basic sanity check
        utils.check_freq(frequency)
        utils.check_channels(channels)
        utils.check_application(application)

        self._freq = frequency
        self._channels = channels
        self._mode = application

        # initialize state
        super(OpusEncoder, self).__init__()

    def _get_state_size(self):
        return llinterface.encoder_get_size(self._channels)

    def _init_state(self):
        llinterface.encoder_init(
                self._state,
                self._freq,
                self._channels,
                self._mode,
                )

    # Generic CTLs
    def reset_state(self):
        ctl.encoder_reset_state(self._state)

    @property
    def final_range(self):
        return ctl.encoder_get_final_range(self._state)

    @property
    def pitch(self):
        return ctl.encoder_get_pitch(self._state)

    @property
    def bandwidth(self):
        return ctl.encoder_get_bandwidth(self._state)

    # Encoder CTLs
    @bandwidth.setter
    def bandwidth(self, value):
        ctl.encoder_set_bandwidth(self._state, value)

    @property
    def complexity(self):
        return ctl.encoder_get_complexity(self._state)

    @complexity.setter
    def complexity(self, value):
        ctl.encoder_set_complexity(self._state, value)

    @property
    def bitrate(self):
        return ctl.encoder_get_bitrate(self._state)

    @bitrate.setter
    def bitrate(self, value):
        ctl.encoder_set_bitrate(self._state, value)

    @property
    def vbr(self):
        return ctl.encoder_get_vbr(self._state)

    @vbr.setter
    def vbr(self, value):
        ctl.encoder_set_vbr(self._state, value)

    @property
    def vbr_constraint(self):
        return ctl.encoder_get_vbr_constraint(self._state)

    @vbr_constraint.setter
    def vbr_constraint(self, value):
        ctl.encoder_set_vbr_constraint(self._state, value)

    @property
    def force_channels(self):
        return ctl.encoder_get_force_channels(self._state)

    @force_channels.setter
    def force_channels(self, value):
        ctl.encoder_set_force_channels(self._state, value)

    @property
    def max_bandwidth(self):
        return ctl.encoder_get_max_bandwidth(self._state)

    @max_bandwidth.setter
    def max_bandwidth(self, value):
        ctl.encoder_set_max_bandwidth(self._state, value)

    @property
    def signal(self):
        return ctl.encoder_get_signal(self._state)

    @signal.setter
    def signal(self, value):
        ctl.encoder_set_signal(self._state, value)

    @property
    def application(self):
        return ctl.encoder_get_application(self._state)

    @application.setter
    def application(self, value):
        ctl.encoder_set_application(self._state, value)

    @property
    def sample_rate(self):
        # XXX This is really just the frequency specified in the ctor...
        # Should the CTL request be completely removed?
        return ctl.encoder_get_sample_rate(self._state)

    @property
    def lookahead(self):
        return ctl.encoder_get_lookahead(self._state)

    @property
    def inband_fec(self):
        return ctl.encoder_get_inband_fec(self._state)

    @inband_fec.setter
    def inband_fec(self, value):
        ctl.encoder_set_inband_fec(self._state, value)

    @property
    def packet_loss_perc(self):
        return ctl.encoder_get_packet_loss_perc(self._state)

    @packet_loss_perc.setter
    def packet_loss_perc(self, value):
        ctl.encoder_set_packet_loss_perc(self._state, value)

    @property
    def dtx(self):
        return ctl.encoder_get_dtx(self._state)

    @dtx.setter
    def dtx(self, value):
        ctl.encoder_set_dtx(self._state, value)

    @property
    def lsb_depth(self):
        return ctl.encoder_get_lsb_depth(self._state)

    @lsb_depth.setter
    def lsb_depth(self, value):
        ctl.encoder_set_lsb_depth(self._state, value)

    @property
    def last_packet_duration(self):
        return ctl.encoder_get_last_packet_duration(self._state)

    @property
    def expert_frame_duration(self):
        return ctl.encoder_get_expert_frame_duration(self._state)

    @expert_frame_duration.setter
    def expert_frame_duration(self, value):
        ctl.encoder_set_expert_frame_duration(self._state, value)

    @property
    def prediction_disabled(self):
        return ctl.encoder_get_prediction_disabled(self._state)

    @prediction_disabled.setter
    def prediction_disabled(self, value):
        ctl.encoder_set_prediction_disabled(self._state, value)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
