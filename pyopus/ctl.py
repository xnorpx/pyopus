"""
This module provides control functions for the Opus encoder and decoder.
It allows setting and getting various parameters to configure the behavior
of the Opus codec instances.

Functions:
    - encoder_set_complexity
    - encoder_get_complexity
    - encoder_set_bitrate
    - encoder_get_bitrate
    - encoder_set_vbr
    - encoder_get_vbr
    - encoder_set_vbr_constraint
    - encoder_get_vbr_constraint
    - encoder_set_force_channels
    - encoder_get_force_channels
    - encoder_set_max_bandwidth
    - encoder_get_max_bandwidth
    - encoder_set_bandwidth
    - encoder_set_signal
    - encoder_get_signal
    - encoder_set_application
    - encoder_get_application
    - encoder_get_sample_rate
    - encoder_get_lookahead
    - encoder_set_inband_fec
    - encoder_get_inband_fec
    - encoder_set_packet_loss_perc
    - encoder_get_packet_loss_perc
    - encoder_set_dtx
    - encoder_get_dtx
    - encoder_set_lsb_depth
    - encoder_get_lsb_depth
    - encoder_get_last_packet_duration
    - encoder_set_expert_frame_duration
    - encoder_get_expert_frame_duration
    - encoder_set_prediction_disabled
    - encoder_get_prediction_disabled
    - encoder_reset_state
    - decoder_reset_state
    - encoder_get_final_range
    - decoder_get_final_range
    - encoder_get_pitch
    - decoder_get_pitch
    - encoder_get_bandwidth
    - decoder_get_bandwidth
    - decoder_set_gain
    - decoder_get_gain
"""

from enum import Enum
from threading import Lock
from typing import Any, Callable

from . import constants
from .binding import ffi
from .constants import OK, OPUS_INVALID_PACKET, OpusError
from .llinterface import decoder_ctl, encoder_ctl
from .utils import strerror

__all__: list[str] = [
    "encoder_set_complexity",
    "encoder_get_complexity",
    "encoder_set_bitrate",
    "encoder_get_bitrate",
    "encoder_set_vbr",
    "encoder_get_vbr",
    "encoder_set_vbr_constraint",
    "encoder_get_vbr_constraint",
    "encoder_set_force_channels",
    "encoder_get_force_channels",
    "encoder_set_max_bandwidth",
    "encoder_get_max_bandwidth",
    "encoder_set_bandwidth",
    "encoder_set_signal",
    "encoder_get_signal",
    "encoder_set_application",
    "encoder_get_application",
    "encoder_get_sample_rate",
    "encoder_get_lookahead",
    "encoder_set_inband_fec",
    "encoder_get_inband_fec",
    "encoder_set_packet_loss_perc",
    "encoder_get_packet_loss_perc",
    "encoder_set_dtx",
    "encoder_get_dtx",
    "encoder_set_lsb_depth",
    "encoder_get_lsb_depth",
    "encoder_get_last_packet_duration",
    "encoder_set_expert_frame_duration",
    "encoder_get_expert_frame_duration",
    "encoder_set_prediction_disabled",
    "encoder_get_prediction_disabled",
    "encoder_reset_state",
    "decoder_reset_state",
    "encoder_get_final_range",
    "decoder_get_final_range",
    "encoder_get_pitch",
    "decoder_get_pitch",
    "encoder_get_bandwidth",
    "decoder_get_bandwidth",
    "decoder_set_gain",
    "decoder_get_gain",
]


class EncoderControlRequest(Enum):
    """Enumeration for Opus encoder control request codes."""

    SET_COMPLEXITY = constants.SET_COMPLEXITY_REQUEST
    GET_COMPLEXITY = constants.GET_COMPLEXITY_REQUEST
    SET_BITRATE = constants.SET_BITRATE_REQUEST
    GET_BITRATE = constants.GET_BITRATE_REQUEST
    SET_VBR = constants.SET_VBR_REQUEST
    GET_VBR = constants.GET_VBR_REQUEST
    SET_VBR_CONSTRAINT = constants.SET_VBR_CONSTRAINT_REQUEST
    GET_VBR_CONSTRAINT = constants.GET_VBR_CONSTRAINT_REQUEST
    SET_FORCE_CHANNELS = constants.SET_FORCE_CHANNELS_REQUEST
    GET_FORCE_CHANNELS = constants.GET_FORCE_CHANNELS_REQUEST
    SET_MAX_BANDWIDTH = constants.SET_MAX_BANDWIDTH_REQUEST
    GET_MAX_BANDWIDTH = constants.GET_MAX_BANDWIDTH_REQUEST
    SET_BANDWIDTH = constants.SET_BANDWIDTH_REQUEST
    SET_SIGNAL = constants.SET_SIGNAL_REQUEST
    GET_SIGNAL = constants.GET_SIGNAL_REQUEST
    SET_APPLICATION = constants.SET_APPLICATION_REQUEST
    GET_APPLICATION = constants.GET_APPLICATION_REQUEST
    GET_SAMPLE_RATE = constants.GET_SAMPLE_RATE_REQUEST
    GET_LOOKAHEAD = constants.GET_LOOKAHEAD_REQUEST
    SET_INBAND_FEC = constants.SET_INBAND_FEC_REQUEST
    GET_INBAND_FEC = constants.GET_INBAND_FEC_REQUEST
    SET_PACKET_LOSS_PERC = constants.SET_PACKET_LOSS_PERC_REQUEST
    GET_PACKET_LOSS_PERC = constants.GET_PACKET_LOSS_PERC_REQUEST
    SET_DTX = constants.SET_DTX_REQUEST
    GET_DTX = constants.GET_DTX_REQUEST
    SET_LSB_DEPTH = constants.SET_LSB_DEPTH_REQUEST
    GET_LSB_DEPTH = constants.GET_LSB_DEPTH_REQUEST
    GET_LAST_PACKET_DURATION = constants.GET_LAST_PACKET_DURATION_REQUEST
    SET_EXPERT_FRAME_DURATION = constants.SET_EXPERT_FRAME_DURATION_REQUEST
    GET_EXPERT_FRAME_DURATION = constants.GET_EXPERT_FRAME_DURATION_REQUEST
    SET_PREDICTION_DISABLED = constants.SET_PREDICTION_DISABLED_REQUEST
    GET_PREDICTION_DISABLED = constants.GET_PREDICTION_DISABLED_REQUEST
    RESET_STATE = constants.RESET_STATE


class DecoderControlRequest(Enum):
    """Enumeration for Opus decoder control request codes."""

    RESET_STATE = constants.RESET_STATE
    GET_FINAL_RANGE = constants.GET_FINAL_RANGE_REQUEST
    GET_PITCH = constants.GET_PITCH_REQUEST
    GET_BANDWIDTH = constants.GET_BANDWIDTH_REQUEST
    SET_GAIN = constants.SET_GAIN_REQUEST
    GET_GAIN = constants.GET_GAIN_REQUEST


def _cast_int(x: int) -> Any:
    """
    Cast an integer to a C int type using ffi.

    Args:
        x (int): The integer to cast.

    Returns:
        Any: The casted C int.
    """
    return ffi.cast("int", x)


def _new_intptr() -> Any:
    """
    Create a new pointer to an int.

    Returns:
        Any: A new C int pointer.
    """
    return ffi.new("int[1]")


def _new_uintptr() -> Any:
    """
    Create a new pointer to an unsigned int.

    Returns:
        Any: A new C unsigned int pointer.
    """
    return ffi.new("unsigned int[1]")


def _set_int(fn: Callable, st: Any, request: EncoderControlRequest, value: int) -> None:
    """
    Set an integer control parameter for the encoder.

    Args:
        fn (Callable): The control function (encoder_ctl).
        st (Any): The encoder state.
        request (EncoderControlRequest): The control request enum.
        value (int): The integer value to set.
    """
    result = fn(st, request.value, _cast_int(value))
    if result != OK:
        raise OpusError(result)


def _get_int(fn: Callable, st: Any, request: EncoderControlRequest) -> int:
    """
    Get an integer control parameter from the encoder.

    Args:
        fn (Callable): The control function (encoder_ctl).
        st (Any): The encoder state.
        request (EncoderControlRequest): The control request enum.

    Returns:
        int: The retrieved integer value.
    """
    result_p = _new_intptr()
    fn(st, request.value, result_p)
    return result_p[0]


def _get_uint(fn: Callable, st: Any, request: EncoderControlRequest) -> int:
    """
    Get an unsigned integer control parameter from the encoder.

    Args:
        fn (Callable): The control function (encoder_ctl).
        st (Any): The encoder state.
        request (EncoderControlRequest): The control request enum.

    Returns:
        int: The retrieved unsigned integer value.
    """
    result_p = _new_uintptr()
    fn(st, request.value, result_p)
    return result_p[0]


def _set_bool(
    fn: Callable, st: Any, request: EncoderControlRequest, value: bool
) -> None:
    """
    Set a boolean control parameter for the encoder.

    Args:
        fn (Callable): The control function (encoder_ctl).
        st (Any): The encoder state.
        request (EncoderControlRequest): The control request enum.
        value (bool): The boolean value to set.
    """
    _set_int(fn, st, request, 1 if value else 0)


def _get_bool(fn: Callable, st: Any, request: EncoderControlRequest) -> bool:
    """
    Get a boolean control parameter from the encoder.

    Args:
        fn (Callable): The control function (encoder_ctl).
        st (Any): The encoder state.
        request (EncoderControlRequest): The control request enum.

    Returns:
        bool: The retrieved boolean value.
    """
    return _get_int(fn, st, request) != 0


# Encoder CTLs
def encoder_set_complexity(st: Any, x: int) -> None:
    """
    Set the complexity level of the encoder.

    Args:
        st (Any): The encoder state.
        x (int): Complexity level to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_COMPLEXITY, x)


def encoder_get_complexity(st: Any) -> int:
    """
    Get the current complexity level of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Current complexity level.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_COMPLEXITY)


def encoder_set_bitrate(st: Any, x: int) -> None:
    """
    Set the bitrate of the encoder.

    Args:
        st (Any): The encoder state.
        x (int): Bitrate value to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_BITRATE, x)


def encoder_get_bitrate(st: Any) -> int:
    """
    Get the current bitrate of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Current bitrate value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_BITRATE)


def encoder_set_vbr(st: Any, enabled: bool) -> None:
    """
    Enable or disable Variable Bitrate (VBR) in the encoder.

    Args:
        st (Any): The encoder state.
        enabled (bool): True to enable VBR, False to disable.
    """
    _set_bool(encoder_ctl, st, EncoderControlRequest.SET_VBR, enabled)


def encoder_get_vbr(st: Any) -> bool:
    """
    Get the current Variable Bitrate (VBR) setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        bool: True if VBR is enabled, False otherwise.
    """
    return _get_bool(encoder_ctl, st, EncoderControlRequest.GET_VBR)


def encoder_set_vbr_constraint(st: Any, constrained: bool) -> None:
    """
    Enable or disable VBR constraint in the encoder.

    Args:
        st (Any): The encoder state.
        constrained (bool): True to enable VBR constraint, False to disable.
    """
    _set_bool(encoder_ctl, st, EncoderControlRequest.SET_VBR_CONSTRAINT, constrained)


def encoder_get_vbr_constraint(st: Any) -> bool:
    """
    Get the current VBR constraint setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        bool: True if VBR constraint is enabled, False otherwise.
    """
    return _get_bool(encoder_ctl, st, EncoderControlRequest.GET_VBR_CONSTRAINT)


def encoder_set_force_channels(st: Any, x: int) -> None:
    """
    Set the number of channels the encoder should force.

    Args:
        st (Any): The encoder state.
        x (int): Number of channels to force.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_FORCE_CHANNELS, x)


def encoder_get_force_channels(st: Any) -> int:
    """
    Get the current number of channels the encoder is forcing.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Number of channels being forced.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_FORCE_CHANNELS)


def encoder_set_max_bandwidth(st: Any, x: int) -> None:
    """
    Set the maximum bandwidth for the encoder.

    Args:
        st (Any): The encoder state.
        x (int): Maximum bandwidth value to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_MAX_BANDWIDTH, x)


def encoder_get_max_bandwidth(st: Any) -> int:
    """
    Get the current maximum bandwidth of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Current maximum bandwidth value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_MAX_BANDWIDTH)


def encoder_set_bandwidth(st: Any, x: int) -> None:
    """
    Set the bandwidth of the encoder.

    Args:
        st (Any): The encoder state.
        x (int): Bandwidth value to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_BANDWIDTH, x)


def encoder_set_signal(st: Any, x: int) -> None:
    """
    Set the signal type of the encoder.

    Args:
        st (Any): The encoder state.
        x (int): Signal type value to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_SIGNAL, x)


def encoder_get_signal(st: Any) -> int:
    """
    Get the current signal type of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Current signal type value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_SIGNAL)


def encoder_set_application(st: Any, x: int) -> None:
    """
    Set the application mode of the encoder.

    Args:
        st (Any): The encoder state.
        x (int): Application mode value to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_APPLICATION, x)


def encoder_get_application(st: Any) -> int:
    """
    Get the current application mode of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Current application mode value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_APPLICATION)


def encoder_get_sample_rate(st: Any) -> int:
    """
    Get the sample rate of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Sample rate in Hz.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_SAMPLE_RATE)


def encoder_get_lookahead(st: Any) -> int:
    """
    Get the lookahead value of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Lookahead value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_LOOKAHEAD)


def encoder_set_inband_fec(st: Any, enabled: bool) -> None:
    """
    Enable or disable in-band Forward Error Correction (FEC) in the encoder.

    Args:
        st (Any): The encoder state.
        enabled (bool): True to enable FEC, False to disable.
    """
    _set_bool(encoder_ctl, st, EncoderControlRequest.SET_INBAND_FEC, enabled)


def encoder_get_inband_fec(st: Any) -> bool:
    """
    Get the current in-band Forward Error Correction (FEC) setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        bool: True if in-band FEC is enabled, False otherwise.
    """
    return _get_bool(encoder_ctl, st, EncoderControlRequest.GET_INBAND_FEC)


def encoder_set_packet_loss_perc(st: Any, x: int) -> None:
    """
    Set the packet loss percentage for the encoder.

    Args:
        st (Any): The encoder state.
        x (int): Packet loss percentage to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_PACKET_LOSS_PERC, x)


def encoder_get_packet_loss_perc(st: Any) -> int:
    """
    Get the current packet loss percentage setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Current packet loss percentage.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_PACKET_LOSS_PERC)


def encoder_set_dtx(st: Any, enabled: bool) -> None:
    """
    Enable or disable Discontinuous Transmission (DTX) in the encoder.

    Args:
        st (Any): The encoder state.
        enabled (bool): True to enable DTX, False to disable.
    """
    _set_bool(encoder_ctl, st, EncoderControlRequest.SET_DTX, enabled)


def encoder_get_dtx(st: Any) -> bool:
    """
    Get the current Discontinuous Transmission (DTX) setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        bool: True if DTX is enabled, False otherwise.
    """
    return _get_bool(encoder_ctl, st, EncoderControlRequest.GET_DTX)


def encoder_set_lsb_depth(st: Any, x: int) -> None:
    """
    Set the Least Significant Bit (LSB) depth for the encoder.

    Args:
        st (Any): The encoder state.
        x (int): LSB depth value to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_LSB_DEPTH, x)


def encoder_get_lsb_depth(st: Any) -> int:
    """
    Get the current Least Significant Bit (LSB) depth of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Current LSB depth value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_LSB_DEPTH)


def encoder_get_last_packet_duration(st: Any) -> int:
    """
    Get the duration of the last encoded packet.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Duration of the last packet in samples.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_LAST_PACKET_DURATION)


def encoder_set_expert_frame_duration(st: Any, x: int) -> None:
    """
    Set the expert frame duration for the encoder.

    Args:
        st (Any): The encoder state.
        x (int): Expert frame duration value to set.
    """
    _set_int(encoder_ctl, st, EncoderControlRequest.SET_EXPERT_FRAME_DURATION, x)


def encoder_get_expert_frame_duration(st: Any) -> int:
    """
    Get the current expert frame duration setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Current expert frame duration value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_EXPERT_FRAME_DURATION)


def encoder_set_prediction_disabled(st: Any, disabled: bool) -> None:
    """
    Enable or disable prediction in the encoder.

    Args:
        st (Any): The encoder state.
        disabled (bool): True to disable prediction, False to enable.
    """
    _set_bool(encoder_ctl, st, EncoderControlRequest.SET_PREDICTION_DISABLED, disabled)


def encoder_get_prediction_disabled(st: Any) -> bool:
    """
    Get the current prediction disabled setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        bool: True if prediction is disabled, False otherwise.
    """
    return _get_bool(encoder_ctl, st, EncoderControlRequest.GET_PREDICTION_DISABLED)


# Generic CTLs
def encoder_reset_state(st: Any) -> None:
    """
    Reset the encoder state.

    Args:
        st (Any): The encoder state.
    """
    encoder_ctl(st, EncoderControlRequest.RESET_STATE.value)


def decoder_reset_state(st: Any) -> None:
    """
    Reset the decoder state.

    Args:
        st (Any): The decoder state.
    """
    decoder_ctl(st, DecoderControlRequest.RESET_STATE.value)


def encoder_get_final_range(st: Any) -> int:
    """
    Get the final range value of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Final range value.
    """
    return _get_uint(encoder_ctl, st, EncoderControlRequest.GET_FINAL_RANGE)


def decoder_get_final_range(st: Any) -> int:
    """
    Get the final range value of the decoder.

    Args:
        st (Any): The decoder state.

    Returns:
        int: Final range value.
    """
    return _get_uint(decoder_ctl, st, DecoderControlRequest.GET_FINAL_RANGE)


def encoder_get_pitch(st: Any) -> int:
    """
    Get the pitch setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Pitch value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_PITCH)


def decoder_get_pitch(st: Any) -> int:
    """
    Get the pitch setting of the decoder.

    Args:
        st (Any): The decoder state.

    Returns:
        int: Pitch value.
    """
    return _get_int(decoder_ctl, st, DecoderControlRequest.GET_PITCH)


def encoder_get_bandwidth(st: Any) -> int:
    """
    Get the bandwidth setting of the encoder.

    Args:
        st (Any): The encoder state.

    Returns:
        int: Bandwidth value.
    """
    return _get_int(encoder_ctl, st, EncoderControlRequest.GET_BANDWIDTH)


def decoder_get_bandwidth(st: Any) -> int:
    """
    Get the bandwidth setting of the decoder.

    Args:
        st (Any): The decoder state.

    Returns:
        int: Bandwidth value.
    """
    return _get_int(decoder_ctl, st, DecoderControlRequest.GET_BANDWIDTH)


# Decoder CTLs
def decoder_set_gain(st: Any, x: int) -> None:
    """
    Set the gain of the decoder.

    Args:
        st (Any): The decoder state.
        x (int): Gain value to set.
    """
    _set_int(decoder_ctl, st, DecoderControlRequest.SET_GAIN, x)


def decoder_get_gain(st: Any) -> int:
    """
    Get the current gain of the decoder.

    Args:
        st (Any): The decoder state.

    Returns:
        int: Current gain value.
    """
    return _get_int(decoder_ctl, st, DecoderControlRequest.GET_GAIN)
