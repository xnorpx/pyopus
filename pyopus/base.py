# -*- coding: utf-8 -*-

'''Opus encoder.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'ManagedState',
        'OpusCodec',
        ]

from . import binding


class ManagedState(object):
    '''Internal class for managing a chunk of memory storing codec state.'''

    def __init__(self):
        self._state = binding.ffi.new('char[]', self._get_state_size())
        self._init_state()

    def _get_state_size(self):
        raise NotImplementedError

    def _init_state(self):
        raise NotImplementedError


class OpusCodec(ManagedState):
    '''Baseclass for Opus encoder and decoder.'''

    def __init__(self):
        super(OpusCodec, self).__init__()


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
