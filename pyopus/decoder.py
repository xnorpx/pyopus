# -*- coding: utf-8 -*-

'''Opus decoder.'''

from __future__ import unicode_literals, absolute_import

__all__ = [
        'OpusDecoder',
        'FloatOpusDecoder',
        ]

from threading import Lock

from . import base
from . import binding
from . import llinterface
from . import ctl
from . import utils

# Maximum packet duration per channel is 60ms, which is 2880 samples
# under 48000Hz. This is multiplied by channel count in decoder init to give
# the memory buffer's size.
PCM_BUFFER_SAMPLES = 2880

# 2.5ms, which is the minimum allowed frame duration
MIN_FRAME_DURATION = 0.0025


class BaseOpusDecoder(base.OpusCodec):
    '''Opus decoder.'''

    _buf_type = None
    _decoder_fn = None

    def __init__(self, frequency=48000, channels=2):
        # basic sanity check
        utils.check_freq(frequency)
        utils.check_channels(channels)

        self._freq = frequency
        self._channels = channels

        self._min_frame_samples = int(MIN_FRAME_DURATION * frequency)

        # initialize state
        super(BaseOpusDecoder, self).__init__()

        # initialize decoder output buffer and locking
        self._pcm = binding.ffi.new(
                self._buf_type,
                PCM_BUFFER_SAMPLES * channels
                )
        self._buf_lock = Lock()

    def _get_state_size(self):
        return llinterface.decoder_get_size(self._channels)

    def _init_state(self):
        llinterface.decoder_init(self._state, self._freq, self._channels)

    # Fast path without PLC or FEC
    def decode(self, data):
        with self._buf_lock:
            num_samples = self._decoder_fn(
                    self._state,
                    data,
                    len(data),
                    self._pcm,
                    PCM_BUFFER_SAMPLES,
                    0,
                    )
            return list(self._pcm[0:num_samples])

    # Generic (slow) path for PLC and FEC
    def decode_plc_fec(self, data=None, frame_duration=None, decode_fec=False):
        if data is None or decode_fec:
            if frame_duration is None:
                raise ValueError(
                        'duration of missing audio (or the frame length) '
                        'must be given in the case of PLC or FEC; please '
                        'specify the duration in numbers of 2.5ms frames in '
                        'these cases.'
                        )
            frame_size = frame_duration * self._min_frame_samples
        else:
            frame_size = PCM_BUFFER_SAMPLES

        len_data = len(data) if data is not None else 0

        with self._buf_lock:
            num_samples = self.decoder_fn(
                    self._state,
                    data,
                    len_data,
                    self._pcm,
                    frame_size,
                    1 if decode_fec else 0,
                    )
            return list(self._pcm[0:num_samples])

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


class OpusDecoder(BaseOpusDecoder):
    _buf_type = 'short[]'
    _decoder_fn = staticmethod(llinterface.decode)


class FloatOpusDecoder(BaseOpusDecoder):
    _buf_type = 'float[]'
    _decoder_fn = staticmethod(llinterface.decode_float)


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
