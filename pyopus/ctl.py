# -*- coding: utf-8 -*-

'''Low-level Opus CTLs.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'encoder_set_complexity',
        'encoder_get_complexity',
        'encoder_set_bitrate',
        'encoder_get_bitrate',
        'encoder_set_vbr',
        'encoder_get_vbr',
        'encoder_set_vbr_constraint',
        'encoder_get_vbr_constraint',
        'encoder_set_force_channels',
        'encoder_get_force_channels',
        'encoder_set_max_bandwidth',
        'encoder_get_max_bandwidth',
        'encoder_set_bandwidth',
        'encoder_set_signal',
        'encoder_get_signal',
        'encoder_set_application',
        'encoder_get_application',
        'encoder_get_sample_rate',
        'encoder_get_lookahead',
        'encoder_set_inbound_fec',
        'encoder_get_inbound_fec',
        'encoder_set_packet_loss_perc',
        'encoder_get_packet_loss_perc',
        'encoder_set_dtx',
        'encoder_get_dtx',
        'encoder_set_lsb_depth',
        'encoder_get_lsb_depth',
        'encoder_get_last_packet_duration',
        'encoder_set_expert_frame_duration',
        'encoder_get_expert_frame_duration',
        'encoder_set_prediction_disabled',
        'encoder_get_prediction_disabled',
        ]

import decorator

from .binding import ffi
from . import constants
from .llinterface import encoder_ctl, decoder_ctl


def _cast_int(x):
    return ffi.cast('int', x)


def _new_intptr():
    return ffi.new('int[1]')


def _set_int(fn, st, request, value):
    return fn(st, request, _cast_int(value))


def _get_int(fn, st, request):
    result_p = _new_intptr()
    fn(st, request, result_p)
    return result_p[0]


def _set_bool(fn, st, request, value):
    return fn(st, request, _cast_int(1 if value else 0))


def _get_bool(fn, st, request):
    return _get_int(fn, st, request) != 0


# Encoder CTLs
def encoder_set_complexity(st, x):
    _set_int(encoder_ctl, st, constants.SET_COMPLEXITY_REQUEST, x)


def encoder_get_complexity(st):
    return _get_int(encoder_ctl, st, constants.GET_COMPLEXITY_REQUEST)


def encoder_set_bitrate(st, x):
    _set_int(encoder_ctl, st, constants.SET_BITRATE_REQUEST, x)


def encoder_get_bitrate(st):
    return _get_int(encoder_ctl, st, constants.GET_BITRATE_REQUEST)


def encoder_set_vbr(st, enabled):
    _set_bool(encoder_ctl, st, constants.SET_VBR_REQUEST, enabled)


def encoder_get_vbr(st):
    return _get_bool(encoder_ctl, st, constants.GET_VBR_REQUEST)


def encoder_set_vbr_constraint(st, constrained):
    _set_bool(
            encoder_ctl,
            st,
            constants.SET_VBR_CONSTRAINT_REQUEST,
            constrained,
            )


def encoder_get_vbr_constraint(st):
    return _get_bool(encoder_ctl, st, constants.GET_VBR_CONSTRAINT_REQUEST)


def encoder_set_force_channels(st, x):
    _set_int(encoder_ctl, st, constants.SET_FORCE_CHANNELS_REQUEST, x)


def encoder_get_force_channels(st):
    return _get_int(encoder_ctl, st, constants.GET_FORCE_CHANNELS_REQUEST)


def encoder_set_max_bandwidth(st, x):
    _set_int(encoder_ctl, st, constants.SET_MAX_BANDWIDTH_REQUEST, x)


def encoder_get_max_bandwidth(st):
    return _get_int(encoder_ctl, st, constants.GET_MAX_BANDWIDTH_REQUEST)


def encoder_set_bandwidth(st, x):
    _set_int(encoder_ctl, st, constants.SET_BANDWIDTH_REQUEST, x)


def encoder_set_signal(st, x):
    _set_int(encoder_ctl, st, constants.SET_SIGNAL_REQUEST, x)


def encoder_get_signal(st):
    return _get_int(encoder_ctl, st, constants.GET_SIGNAL_REQUEST)


def encoder_set_application(st, x):
    _set_int(encoder_ctl, st, constants.SET_APPLICATION_REQUEST, x)


def encoder_get_application(st):
    return _get_int(encoder_ctl, st, constants.GET_APPLICATION_REQUEST)


def encoder_get_sample_rate(st):
    return _get_int(encoder_ctl, st, constants.GET_SAMPLE_RATE_REQUEST)


def encoder_get_lookahead(st):
    return _get_int(encoder_ctl, st, constants.GET_LOOKAHEAD_REQUEST)


def encoder_set_inbound_fec(st, enabled):
    _set_bool(encoder_ctl, st, constants.SET_INBAND_FEC_REQUEST, enabled)


def encoder_get_inbound_fec(st):
    return _get_bool(encoder_ctl, st, constants.GET_INBAND_FEC_REQUEST)


def encoder_set_packet_loss_perc(st, x):
    _set_int(encoder_ctl, st, constants.SET_PACKET_LOSS_PERC_REQUEST, x)


def encoder_get_packet_loss_perc(st):
    return _get_int(encoder_ctl, st, constants.GET_PACKET_LOSS_PERC_REQUEST)


def encoder_set_dtx(st, enabled):
    _set_bool(encoder_ctl, st, constants.SET_DTX_REQUEST, enabled)


def encoder_get_dtx(st):
    return _get_bool(encoder_ctl, st, constants.GET_DTX_REQUEST)


def encoder_set_lsb_depth(st, x):
    _set_int(encoder_ctl, st, constants.SET_LSB_DEPTH_REQUEST, x)


def encoder_get_lsb_depth(st):
    return _get_int(encoder_ctl, st, constants.GET_LSB_DEPTH_REQUEST)


def encoder_get_last_packet_duration(st):
    return _get_int(
            encoder_ctl,
            st,
            constants.GET_LAST_PACKET_DURATION_REQUEST,
            )


def encoder_set_expert_frame_duration(st, x):
    _set_int(encoder_ctl, st, constants.SET_EXPERT_FRAME_DURATION_REQUEST, x)


def encoder_get_expert_frame_duration(st):
    return _get_int(
            encoder_ctl,
            st,
            constants.GET_EXPERT_FRAME_DURATION_REQUEST,
            )


def encoder_set_prediction_disabled(st, disabled):
    _set_bool(
            encoder_ctl,
            st,
            constants.SET_PREDICTION_DISABLED_REQUEST,
            disabled,
            )


def encoder_get_prediction_disabled(st):
    return _get_bool(
            encoder_ctl,
            st,
            constants.GET_PREDICTION_DISABLED_REQUEST,
            )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
