"""
This module defines and exposes various Opus codec constants organized into Enums.
These constants are used to control and configure Opus encoder and decoder instances.

Classes:
    - OpusError: Enumeration of Opus error codes.
    - EncoderControlRequest: Enumeration of Opus encoder control request codes.
    - DecoderControlRequest: Enumeration of Opus decoder control request codes.
    - OpusApplication: Enumeration of Opus application modes.
    - OpusSignal: Enumeration of Opus signal types.
    - OpusBandwidth: Enumeration of Opus bandwidth options.
    - OpusFrameSize: Enumeration of Opus frame sizes.
"""

from enum import IntEnum
from typing import List

from . import constants
from .binding import C

__all__: List[str] = [
    "OpusError",
    "EncoderControlRequest",
    "DecoderControlRequest",
    "OpusApplication",
    "OpusSignal",
    "OpusBandwidth",
    "OpusFrameSize",
]


class OpusError(IntEnum):
    """
    Enumeration of Opus error codes.

    Attributes:
        OK (int): Success.
        BAD_ARG (int): One or more invalid/out of range arguments.
        BUFFER_TOO_SMALL (int): Not enough bytes allocated in buffer.
        INTERNAL_ERROR (int): An internal error was detected.
        INVALID_PACKET (int): The compressed data passed is corrupted.
        UNIMPLEMENTED (int): Invalid/unsupported request number.
        INVALID_STATE (int): An encoder or decoder structure is invalid or already freed.
        ALLOC_FAIL (int): Memory allocation has failed.
    """

    OK = C.OPUS_OK
    BAD_ARG = C.OPUS_BAD_ARG
    BUFFER_TOO_SMALL = C.OPUS_BUFFER_TOO_SMALL
    INTERNAL_ERROR = C.OPUS_INTERNAL_ERROR
    INVALID_PACKET = C.OPUS_INVALID_PACKET
    UNIMPLEMENTED = C.OPUS_UNIMPLEMENTED
    INVALID_STATE = C.OPUS_INVALID_STATE
    ALLOC_FAIL = C.OPUS_ALLOC_FAIL


class EncoderControlRequest(IntEnum):
    """
    Enumeration of Opus encoder control request codes.

    Attributes:
        SET_APPLICATION (int): Set the encoder's application mode.
        GET_APPLICATION (int): Get the encoder's application mode.
        SET_BITRATE (int): Set the encoder's bitrate.
        GET_BITRATE (int): Get the encoder's bitrate.
        SET_MAX_BANDWIDTH (int): Set the encoder's maximum bandwidth.
        GET_MAX_BANDWIDTH (int): Get the encoder's maximum bandwidth.
        SET_VBR (int): Enable or disable Variable Bitrate (VBR).
        GET_VBR (int): Check if VBR is enabled.
        SET_BANDWIDTH (int): Set the encoder's bandwidth.
        GET_BANDWIDTH (int): Get the encoder's bandwidth.
        SET_COMPLEXITY (int): Set the encoder's complexity.
        GET_COMPLEXITY (int): Get the encoder's complexity.
        SET_INBAND_FEC (int): Enable or disable in-band Forward Error Correction (FEC).
        GET_INBAND_FEC (int): Check if in-band FEC is enabled.
        SET_PACKET_LOSS_PERC (int): Set the packet loss percentage.
        GET_PACKET_LOSS_PERC (int): Get the packet loss percentage.
        SET_DTX (int): Enable or disable Discontinuous Transmission (DTX).
        GET_DTX (int): Check if DTX is enabled.
        SET_VBR_CONSTRAINT (int): Enable or disable VBR constraint.
        GET_VBR_CONSTRAINT (int): Check if VBR constraint is enabled.
        SET_FORCE_CHANNELS (int): Force the number of channels.
        GET_FORCE_CHANNELS (int): Get the number of forced channels.
        SET_SIGNAL (int): Set the signal type.
        GET_SIGNAL (int): Get the signal type.
        GET_LOOKAHEAD (int): Get the encoder's lookahead.
        GET_SAMPLE_RATE (int): Get the encoder's sample rate.
        GET_FINAL_RANGE (int): Get the encoder's final range.
        GET_PITCH (int): Get the encoder's pitch.
        SET_GAIN (int): Set the decoder's gain.
        GET_GAIN (int): Get the decoder's gain.
        SET_LSB_DEPTH (int): Set the Least Significant Bit (LSB) depth.
        GET_LSB_DEPTH (int): Get the LSB depth.
        GET_LAST_PACKET_DURATION (int): Get the duration of the last packet.
        SET_EXPERT_FRAME_DURATION (int): Set the expert frame duration.
        GET_EXPERT_FRAME_DURATION (int): Get the expert frame duration.
        SET_PREDICTION_DISABLED (int): Enable or disable prediction.
        GET_PREDICTION_DISABLED (int): Check if prediction is disabled.
        RESET_STATE (int): Reset the encoder/decoder state.
    """

    SET_APPLICATION = constants.SET_APPLICATION_REQUEST
    GET_APPLICATION = constants.GET_APPLICATION_REQUEST
    SET_BITRATE = constants.SET_BITRATE_REQUEST
    GET_BITRATE = constants.GET_BITRATE_REQUEST
    SET_MAX_BANDWIDTH = constants.SET_MAX_BANDWIDTH_REQUEST
    GET_MAX_BANDWIDTH = constants.GET_MAX_BANDWIDTH_REQUEST
    SET_VBR = constants.SET_VBR_REQUEST
    GET_VBR = constants.GET_VBR_REQUEST
    SET_BANDWIDTH = constants.SET_BANDWIDTH_REQUEST
    GET_BANDWIDTH = constants.GET_BANDWIDTH_REQUEST
    SET_COMPLEXITY = constants.SET_COMPLEXITY_REQUEST
    GET_COMPLEXITY = constants.GET_COMPLEXITY_REQUEST
    SET_INBAND_FEC = constants.SET_INBAND_FEC_REQUEST
    GET_INBAND_FEC = constants.GET_INBAND_FEC_REQUEST
    SET_PACKET_LOSS_PERC = constants.SET_PACKET_LOSS_PERC_REQUEST
    GET_PACKET_LOSS_PERC = constants.GET_PACKET_LOSS_PERC_REQUEST
    SET_DTX = constants.SET_DTX_REQUEST
    GET_DTX = constants.GET_DTX_REQUEST
    SET_VBR_CONSTRAINT = constants.SET_VBR_CONSTRAINT_REQUEST
    GET_VBR_CONSTRAINT = constants.GET_VBR_CONSTRAINT_REQUEST
    SET_FORCE_CHANNELS = constants.SET_FORCE_CHANNELS_REQUEST
    GET_FORCE_CHANNELS = constants.GET_FORCE_CHANNELS_REQUEST
    SET_SIGNAL = constants.SET_SIGNAL_REQUEST
    GET_SIGNAL = constants.GET_SIGNAL_REQUEST
    GET_LOOKAHEAD = constants.GET_LOOKAHEAD_REQUEST
    GET_SAMPLE_RATE = constants.GET_SAMPLE_RATE_REQUEST
    GET_FINAL_RANGE = constants.GET_FINAL_RANGE_REQUEST
    GET_PITCH = constants.GET_PITCH_REQUEST
    SET_GAIN = constants.SET_GAIN_REQUEST
    GET_GAIN = constants.GET_GAIN_REQUEST
    SET_LSB_DEPTH = constants.SET_LSB_DEPTH_REQUEST
    GET_LSB_DEPTH = constants.GET_LSB_DEPTH_REQUEST
    GET_LAST_PACKET_DURATION = constants.GET_LAST_PACKET_DURATION_REQUEST
    SET_EXPERT_FRAME_DURATION = constants.SET_EXPERT_FRAME_DURATION_REQUEST
    GET_EXPERT_FRAME_DURATION = constants.GET_EXPERT_FRAME_DURATION_REQUEST
    SET_PREDICTION_DISABLED = constants.SET_PREDICTION_DISABLED_REQUEST
    GET_PREDICTION_DISABLED = constants.GET_PREDICTION_DISABLED_REQUEST
    RESET_STATE = constants.RESET_STATE


class DecoderControlRequest(IntEnum):
    """
    Enumeration of Opus decoder control request codes.

    Attributes:
        RESET_STATE (int): Reset the decoder state.
        GET_FINAL_RANGE (int): Get the decoder's final range.
        GET_PITCH (int): Get the decoder's pitch.
        GET_BANDWIDTH (int): Get the decoder's bandwidth.
        SET_GAIN (int): Set the decoder's gain.
        GET_GAIN (int): Get the decoder's gain.
    """

    RESET_STATE = constants.RESET_STATE
    GET_FINAL_RANGE = constants.GET_FINAL_RANGE_REQUEST
    GET_PITCH = constants.GET_PITCH_REQUEST
    GET_BANDWIDTH = constants.GET_BANDWIDTH_REQUEST
    SET_GAIN = constants.SET_GAIN_REQUEST
    GET_GAIN = constants.GET_GAIN_REQUEST


class OpusApplication(IntEnum):
    """
    Enumeration of Opus application modes.

    Attributes:
        VOIP (int): Voice over IP.
        AUDIO (int): General audio.
        RESTRICTED_LOWDELAY (int): Low-delay audio.
    """

    VOIP = constants.APPLICATION_VOIP
    AUDIO = constants.APPLICATION_AUDIO
    RESTRICTED_LOWDELAY = constants.APPLICATION_RESTRICTED_LOWDELAY


class OpusSignal(IntEnum):
    """
    Enumeration of Opus signal types.

    Attributes:
        VOICE (int): Voice signal.
        MUSIC (int): Music signal.
    """

    VOICE = constants.SIGNAL_VOICE
    MUSIC = constants.SIGNAL_MUSIC


class OpusBandwidth(IntEnum):
    """
    Enumeration of Opus bandwidth options.

    Attributes:
        NARROWBAND (int): Narrowband (4 kHz).
        MEDIUMBAND (int): Medium-band (6 kHz).
        WIDEBAND (int): Wideband (8 kHz).
        SUPERWIDEBAND (int): Super-wideband (12 kHz).
        FULLBAND (int): Fullband (20 kHz).
    """

    NARROWBAND = constants.BANDWIDTH_NARROWBAND
    MEDIUMBAND = constants.BANDWIDTH_MEDIUMBAND
    WIDEBAND = constants.BANDWIDTH_WIDEBAND
    SUPERWIDEBAND = constants.BANDWIDTH_SUPERWIDEBAND
    FULLBAND = constants.BANDWIDTH_FULLBAND


class OpusFrameSize(IntEnum):
    """
    Enumeration of Opus frame sizes.

    Attributes:
        ARG (int): Argument frame size.
        _2_5_MS (int): 2.5 milliseconds.
        _5_MS (int): 5 milliseconds.
        _10_MS (int): 10 milliseconds.
        _20_MS (int): 20 milliseconds.
        _40_MS (int): 40 milliseconds.
        _60_MS (int): 60 milliseconds.
    """

    ARG = constants.FRAMESIZE_ARG
    _2_5_MS = constants.FRAMESIZE_2_5_MS
    _5_MS = constants.FRAMESIZE_5_MS
    _10_MS = constants.FRAMESIZE_10_MS
    _20_MS = constants.FRAMESIZE_20_MS
    _40_MS = constants.FRAMESIZE_40_MS
    _60_MS = constants.FRAMESIZE_60_MS


class MiscConstants(IntEnum):
    """
    Enumeration of miscellaneous Opus constants.

    Attributes:
        AUTO (int): Automatic setting.
        BITRATE_MAX (int): Maximum bitrate.
    """

    AUTO = constants.AUTO
    BITRATE_MAX = constants.BITRATE_MAX
