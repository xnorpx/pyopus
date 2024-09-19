"""
This module provides Python bindings for the Opus codec library using cffi.
It includes classes for encoding audio using Opus, handling encoder configurations,
and managing encoding operations with thread safety.

Classes:
    - OpusEncoder: A standard Opus encoder for integer PCM data.
    - FloatOpusEncoder: An Opus encoder for floating-point PCM data.
"""

from threading import Lock
from typing import Any, Callable, Optional

from . import base, binding, ctl, llinterface, utils
from .constants import OK

# Slightly larger than the recommended size of 4000 bytes, which is OK
PAYLOAD_BUFFER_SIZE: int = 4096


class OpusApplicationType(base.Enum):
    """Enumeration for Opus encoder application types."""
    VOIP = 2048  # Replace with actual constant value from constants.APPLICATION_VOIP
    AUDIO = 2049  # Replace with actual constant value from constants.APPLICATION_AUDIO
    RESTRICTED_LOWDELAY = 2051  # Replace with actual constant value from constants.APPLICATION_RESTRICTED_LOWDELAY


class BaseOpusEncoder(base.OpusCodec):
    """
    Base class for Opus encoders, providing common functionality for encoding audio data.

    Attributes:
        _encoder_fn (Callable): The encoding function to use (e.g., encode or encode_float).
        _freq (int): Sampling frequency in Hz.
        _channels (int): Number of audio channels.
        _mode (OpusApplicationType): Encoding application mode.
        _out (Any): Output buffer for encoded data.
        _buf (Any): Buffer interface to the output buffer.
        _buf_lock (Lock): Lock to ensure thread-safe access to the output buffer.
    """

    _encoder_fn: Optional[Callable] = None

    def __init__(self, frequency: int, channels: int, application: OpusApplicationType) -> None:
        """
        Initialize the Opus encoder with the specified frequency, channels, and application.

        Args:
            frequency (int): Sampling rate in Hz.
            channels (int): Number of audio channels.
            application (OpusApplicationType): The encoding application mode.

        Raises:
            ValueError: If frequency, channels, or application are not supported.
        """
        # Basic sanity checks
        utils.check_freq(frequency)
        utils.check_channels(channels)
        utils.check_application(application.value)

        self._freq: int = frequency
        self._channels: int = channels
        self._mode: OpusApplicationType = application

        # Dispatch to encode functions with different sanity checking based on channel count
        self.encode: Callable[[bytes], bytes] = self._stereo_encode if channels == 2 else self._mono_encode

        # Initialize state
        super().__init__()

        # Output payload buffer
        # Since the codec is stateful, allowing reentrancy is pointless.
        # Just make one output buffer to avoid repeated memory allocations (and deallocations),
        # and lock it properly.
        self._out: Any = binding.ffi.new("char[]", PAYLOAD_BUFFER_SIZE)
        self._buf: Any = binding.ffi.buffer(self._out)
        self._buf_lock: Lock = Lock()

    def _get_state_size(self) -> int:
        """
        Retrieve the size of the encoder state based on the number of channels.

        Returns:
            int: Size of the encoder state in bytes.
        """
        return llinterface.encoder_get_size(self._channels)

    def _init_state(self) -> None:
        """
        Initialize the encoder state with the specified frequency, channels, and application.
        """
        llinterface.encoder_init(
            self._state,
            self._freq,
            self._channels,
            self._mode.value,
        )

    def _stereo_encode(self, pcm: bytes) -> bytes:
        """
        Encode stereo PCM data.

        Args:
            pcm (bytes): PCM audio data (int16) for stereo channels.

        Raises:
            ValueError: If PCM data length is not even for stereo input.

        Returns:
            bytes: Encoded Opus data.
        """
        # Basic frame-size check
        frame_size, rem = divmod(len(pcm), 2)
        if rem != 0:
            raise ValueError("PCM data length is not even for stereo input")

        return self._do_encode(pcm, frame_size)

    def _mono_encode(self, pcm: bytes) -> bytes:
        """
        Encode mono PCM data.

        Args:
            pcm (bytes): PCM audio data (int16) for mono channel.

        Returns:
            bytes: Encoded Opus data.
        """
        return self._do_encode(pcm, len(pcm))

    def _do_encode(self, pcm: bytes, frame_size: int) -> bytes:
        """
        Perform the actual encoding of PCM data.

        Args:
            pcm (bytes): PCM audio data (int16 or float).
            frame_size (int): Number of samples per channel.

        Returns:
            bytes: Encoded Opus data.
        """
        with self._buf_lock:
            len_payload = self._encoder_fn(
                self._state,
                pcm,
                frame_size,
                self._out,
                PAYLOAD_BUFFER_SIZE,
            )
            return self._buf[:len_payload]

    # Generic CTLs

    def reset_state(self) -> None:
        """
        Reset the encoder state.
        """
        ctl.encoder_reset_state(self._state)

    @property
    def final_range(self) -> int:
        """
        Get the final range of the encoder.

        Returns:
            int: Final range value.
        """
        return ctl.encoder_get_final_range(self._state)

    @property
    def pitch(self) -> int:
        """
        Get the pitch setting of the encoder.

        Returns:
            int: Pitch value.
        """
        return ctl.encoder_get_pitch(self._state)

    @property
    def bandwidth(self) -> int:
        """
        Get the bandwidth setting of the encoder.

        Returns:
            int: Bandwidth value.
        """
        return ctl.encoder_get_bandwidth(self._state)

    @bandwidth.setter
    def bandwidth(self, value: int) -> None:
        """
        Set the bandwidth setting of the encoder.

        Args:
            value (int): Bandwidth value to set.
        """
        ctl.encoder_set_bandwidth(self._state, value)

    @property
    def complexity(self) -> int:
        """
        Get the complexity setting of the encoder.

        Returns:
            int: Complexity value.
        """
        return ctl.encoder_get_complexity(self._state)

    @complexity.setter
    def complexity(self, value: int) -> None:
        """
        Set the complexity setting of the encoder.

        Args:
            value (int): Complexity value to set.
        """
        ctl.encoder_set_complexity(self._state, value)

    @property
    def bitrate(self) -> int:
        """
        Get the bitrate setting of the encoder.

        Returns:
            int: Bitrate value.
        """
        return ctl.encoder_get_bitrate(self._state)

    @bitrate.setter
    def bitrate(self, value: int) -> None:
        """
        Set the bitrate setting of the encoder.

        Args:
            value (int): Bitrate value to set.
        """
        ctl.encoder_set_bitrate(self._state, value)

    @property
    def vbr(self) -> bool:
        """
        Get the VBR (Variable Bitrate) setting of the encoder.

        Returns:
            bool: VBR enabled or not.
        """
        return ctl.encoder_get_vbr(self._state)

    @vbr.setter
    def vbr(self, value: bool) -> None:
        """
        Set the VBR (Variable Bitrate) setting of the encoder.

        Args:
            value (bool): Enable or disable VBR.
        """
        ctl.encoder_set_vbr(self._state, value)

    @property
    def vbr_constraint(self) -> bool:
        """
        Get the VBR constraint setting of the encoder.

        Returns:
            bool: VBR constraint enabled or not.
        """
        return ctl.encoder_get_vbr_constraint(self._state)

    @vbr_constraint.setter
    def vbr_constraint(self, value: bool) -> None:
        """
        Set the VBR constraint setting of the encoder.

        Args:
            value (bool): Enable or disable VBR constraint.
        """
        ctl.encoder_set_vbr_constraint(self._state, value)

    @property
    def force_channels(self) -> int:
        """
        Get the force channels setting of the encoder.

        Returns:
            int: Number of channels forced.
        """
        return ctl.encoder_get_force_channels(self._state)

    @force_channels.setter
    def force_channels(self, value: int) -> None:
        """
        Set the force channels setting of the encoder.

        Args:
            value (int): Number of channels to force.
        """
        ctl.encoder_set_force_channels(self._state, value)

    @property
    def max_bandwidth(self) -> int:
        """
        Get the maximum bandwidth setting of the encoder.

        Returns:
            int: Maximum bandwidth value.
        """
        return ctl.encoder_get_max_bandwidth(self._state)

    @max_bandwidth.setter
    def max_bandwidth(self, value: int) -> None:
        """
        Set the maximum bandwidth setting of the encoder.

        Args:
            value (int): Maximum bandwidth value to set.
        """
        ctl.encoder_set_max_bandwidth(self._state, value)

    @property
    def signal(self) -> int:
        """
        Get the signal type setting of the encoder.

        Returns:
            int: Signal type value.
        """
        return ctl.encoder_get_signal(self._state)

    @signal.setter
    def signal(self, value: int) -> None:
        """
        Set the signal type setting of the encoder.

        Args:
            value (int): Signal type value to set.
        """
        ctl.encoder_set_signal(self._state, value)

    @property
    def application(self) -> OpusApplicationType:
        """
        Get the application mode of the encoder.

        Returns:
            OpusApplicationType: Current application mode.
        """
        return OpusApplicationType(ctl.encoder_get_application(self._state))

    @application.setter
    def application(self, value: OpusApplicationType) -> None:
        """
        Set the application mode of the encoder.

        Args:
            value (OpusApplicationType): Application mode to set.
        """
        ctl.encoder_set_application(self._state, value.value)

    @property
    def sample_rate(self) -> int:
        """
        Get the sample rate of the encoder.

        Returns:
            int: Sample rate in Hz.
        """
        # XXX This is really just the frequency specified in the constructor...
        # Should the CTL request be completely removed?
        return ctl.encoder_get_sample_rate(self._state)

    @property
    def lookahead(self) -> int:
        """
        Get the lookahead setting of the encoder.

        Returns:
            int: Lookahead value.
        """
        return ctl.encoder_get_lookahead(self._state)

    @property
    def inband_fec(self) -> bool:
        """
        Get the in-band FEC (Forward Error Correction) setting of the encoder.

        Returns:
            bool: In-band FEC enabled or not.
        """
        return ctl.encoder_get_inband_fec(self._state)

    @inband_fec.setter
    def inband_fec(self, value: bool) -> None:
        """
        Set the in-band FEC (Forward Error Correction) setting of the encoder.

        Args:
            value (bool): Enable or disable in-band FEC.
        """
        ctl.encoder_set_inband_fec(self._state, value)

    @property
    def packet_loss_perc(self) -> int:
        """
        Get the packet loss percentage setting of the encoder.

        Returns:
            int: Packet loss percentage.
        """
        return ctl.encoder_get_packet_loss_perc(self._state)

    @packet_loss_perc.setter
    def packet_loss_perc(self, value: int) -> None:
        """
        Set the packet loss percentage setting of the encoder.

        Args:
            value (int): Packet loss percentage to set.
        """
        ctl.encoder_set_packet_loss_perc(self._state, value)

    @property
    def dtx(self) -> bool:
        """
        Get the DTX (Discontinuous Transmission) setting of the encoder.

        Returns:
            bool: DTX enabled or not.
        """
        return ctl.encoder_get_dtx(self._state)

    @dtx.setter
    def dtx(self, value: bool) -> None:
        """
        Set the DTX (Discontinuous Transmission) setting of the encoder.

        Args:
            value (bool): Enable or disable DTX.
        """
        ctl.encoder_set_dtx(self._state, value)

    @property
    def lsb_depth(self) -> int:
        """
        Get the LSB (Least Significant Bit) depth setting of the encoder.

        Returns:
            int: LSB depth value.
        """
        return ctl.encoder_get_lsb_depth(self._state)

    @lsb_depth.setter
    def lsb_depth(self, value: int) -> None:
        """
        Set the LSB (Least Significant Bit) depth setting of the encoder.

        Args:
            value (int): LSB depth value to set.
        """
        ctl.encoder_set_lsb_depth(self._state, value)

    @property
    def last_packet_duration(self) -> int:
        """
        Get the duration of the last packet encoded.

        Returns:
            int: Duration of the last packet in samples.
        """
        return ctl.encoder_get_last_packet_duration(self._state)

    @property
    def expert_frame_duration(self) -> int:
        """
        Get the expert frame duration setting of the encoder.

        Returns:
            int: Expert frame duration value.
        """
        return ctl.encoder_get_expert_frame_duration(self._state)

    @expert_frame_duration.setter
    def expert_frame_duration(self, value: int) -> None:
        """
        Set the expert frame duration setting of the encoder.

        Args:
            value (int): Expert frame duration value to set.
        """
        ctl.encoder_set_expert_frame_duration(self._state, value)

    @property
    def prediction_disabled(self) -> bool:
        """
        Get the prediction disabled setting of the encoder.

        Returns:
            bool: Prediction disabled or not.
        """
        return ctl.encoder_get_prediction_disabled(self._state)

    @prediction_disabled.setter
    def prediction_disabled(self, value: bool) -> None:
        """
        Set the prediction disabled setting of the encoder.

        Args:
            value (bool): Enable or disable prediction.
        """
        ctl.encoder_set_prediction_disabled(self._state, value)


class OpusEncoder(BaseOpusEncoder):
    """
    Opus encoder for integer PCM data.

    Inherits from BaseOpusEncoder and sets the encoding function to handle integer PCM data.
    """

    _encoder_fn: Callable[[Any, bytes, int, Any, int], int] = staticmethod(llinterface.encode)


class FloatOpusEncoder(BaseOpusEncoder):
    """
    Opus encoder for floating-point PCM data.

    Inherits from BaseOpusEncoder and sets the encoding function to handle floating-point PCM data.
    """

    _encoder_fn: Callable[[Any, bytes, int, Any, int], int] = staticmethod(llinterface.encode_float)
