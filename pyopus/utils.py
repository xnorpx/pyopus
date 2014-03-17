# -*- coding: utf-8 -*-

'''Internal utilities.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'check_freq',
        'check_channels',
        'check_application',
        ]

from . import constants

_SUPPORTED_FREQS = frozenset({8000, 12000, 16000, 24000, 48000, })
_SUPPORTED_CHANNELS = frozenset({1, 2, })
_SUPPORTED_APPLICATIONS = frozenset({
        constants.APPLICATION_VOIP,
        constants.APPLICATION_AUDIO,
        constants.APPLICATION_RESTRICTED_LOWDELAY,
        })


def check_freq(frequency):
    if frequency not in _SUPPORTED_FREQS:
        raise ValueError('unsupported frequency; please use one of %s' % (
                repr(list(sorted(_SUPPORTED_FREQS))),
                ))


def check_channels(channels):
    if channels not in _SUPPORTED_CHANNELS:
        raise ValueError(
                'unsupported number of channels;'
                ' only 1 or 2 are supported'
                )


def check_application(application):
    if application not in _SUPPORTED_APPLICATIONS:
        raise ValueError(
                'unsupported coding mode;'
                ' please consult Opus docs for the proper constant to use'
                )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
