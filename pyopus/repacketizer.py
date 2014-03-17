# -*- coding: utf-8 -*-

'''Opus repacketizer.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'OpusRepacketizer',
        ]

from . import base
from . import llinterface


class OpusRepacketizer(base.ManagedState):
    '''Opus repacketizer.'''

    def __init__(self):
        # initialize state
        super(OpusRepacketizer, self).__init__()

    def _get_state_size(self):
        return llinterface.repacketizer_get_size()

    def _init_state(self):
        llinterface.repacketizer_init(self._state)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
