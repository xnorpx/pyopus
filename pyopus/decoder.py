"""
This module provides Python bindings for the Opus codec library using cffi.
It includes classes for decoding audio using Opus, handling decoder configurations,
and managing decoding operations with thread safety.

Classes:
    - OpusDecoder: A standard Opus decoder for integer PCM data.
    - FloatOpusDecoder: An Opus decoder for floating-point PCM data.
"""

from threading import Lock
from typing import Any, Callable, Optional, List

from . import base, binding, ctl, llinterface, utils
from .constants import OK, OPUS_INVALID_PACKET  # Assuming OPUS_INVALID_PACKET exists


__all__: list[str] = [
    "OpusDecoder",
    "FloatOpusDecoder",
]

# Maximum packet duration per channel is 60ms, which is 2880 samples
# under 48000Hz. This is multiplied by channel count in decoder init to give
# the memory buffer's size.
PCM_BUFFER_SAMPLES: int = 2880

# 2.5ms, which is the minimum allowed frame duration
MIN_FRAME_DURATION: float = 0.0025


class OpusError(RuntimeError):
    """
    Exception raised for errors returned by Opus library functions.

    Attributes:
        errno (int): The error code returned by the Opus function.
        message (str): A human-readable message describing the error.
    """

    def __init__(self, errno: int):
        """
        Initialize the OpusError with an error number.

        Args:
            errno (int): The error code returned by the Opus function.
        """
        msg = utils.strerror(errno)
        super().__init__(errno, msg)
        self.errno: int = errno
        self.message: str = msg

    def __str__(self) -> str:
        """
        Return the string representation of the error.

        Returns:
            str: A formatted error message.
        """
        return f"[Opus Error {self.errno}] {self.message}"


class OpusApplicationType(base.Enum):
    """Enumeration for Opus application types."""
    VOIP = 2048  # Replace with actual constant value from constants.APPLICATION_VOIP
    AUDIO = 2049  # Replace with actual constant value from constants.APPLICATION_AUDIO
    RESTRICTED_LOWDELAY = 2051  # Replace with actual constant value from constants.APPLICATION_RESTRICTED_LOWDELAY


class BaseOpusDecoder(base.OpusCodec):
    """
    Base class for Opus decoders, providing common functionality for decoding audio data.

    Attributes:
        _decoder_fn (Callable): The decoding function to use (e.g., decode or decode_float).
        _freq (int): Sampling frequency in Hz.
        _channels (int): Number of audio channels.
        _pcm (Any): PCM output buffer.
        _buf_lock (Lock): Lock to ensure thread-safe access to the PCM buffer.
        _min_frame_samples (int): Minimum number of samples per frame based on frame duration.
    """

    _decoder_fn: Optional[Callable[[Any, bytes, int, Any, int, int], int]] = None
    _buf_type: Optional[str] = None

    def __init__(self, frequency: int = 48000, channels: int = 2) -> None:
        """
        Initialize the Opus decoder with the specified frequency and channels.

        Args:
            frequency (int, optional): Sampling rate in Hz. Defaults to 48000.
            channels (int, optional): Number of audio channels. Defaults to 2.

        Raises:
            ValueError: If frequency or channels are not supported.
        """
        # Basic sanity checks
        utils.check_freq(frequency)
        utils.check_channels(channels)

        self._freq: int = frequency
        self._channels: int = channels

        self._min_frame_samples: int = int(MIN_FRAME_DURATION * frequency)

        # Initialize state
        super().__init__()

        # Initialize decoder output buffer and locking
        self._pcm: Any = binding.ffi.new(self._buf_type, PCM_BUFFER_SAMPLES * channels)
        self._buf_lock: Lock = Lock()

    def _get_state_size(self) -> int:
        """
        Retrieve the size of the decoder state based on the number of channels.

        Returns:
            int: Size of the decoder state in bytes.
        """
        return llinterface.decoder_get_size(self._channels)

    def _init_state(self) -> None:
        """
        Initialize the decoder state with the specified frequency and channels.
        """
        llinterface.decoder_init(self._state, self._freq, self._channels)

    def decode(self, data: bytes) -> List[int]:
        """
        Decode Opus data into PCM format without PLC or FEC.

        Args:
            data (bytes): Encoded Opus data.

        Returns:
            List[int]: Decoded PCM data as a list of integers.

        Raises:
            OpusError: If decoding fails.
        """
        with self._buf_lock:
            num_samples = self._decoder_fn(
                self._state,
                data,
                len(data),
                self._pcm,
                PCM_BUFFER_SAMPLES,
                0,
            )
            return list(self._pcm[0 : num_samples * self._channels])

    def decode_plc_fec(
        self,
        data: Optional[bytes] = None,
        frame_duration: Optional[float] = None,
        decode_fec: bool = False
    ) -> List[int]:
        """
        Decode Opus data into PCM format with PLC or FEC.

        Args:
            data (Optional[bytes], optional): Encoded Opus data. Defaults to None.
            frame_duration (Optional[float], optional): Duration of missing audio in seconds. Required if data is None or decode_fec is True. Defaults to None.
            decode_fec (bool, optional): Whether to decode with Forward Error Correction. Defaults to False.

        Returns:
            List[int]: Decoded PCM data as a list of integers.

        Raises:
            ValueError: If frame_duration is not provided when required.
            OpusError: If decoding fails.
        """
        if data is None or decode_fec:
            if frame_duration is None:
                raise ValueError(
                    "Duration of missing audio (or the frame length) "
                    "must be given in the case of PLC or FEC; please "
                    "specify the duration in numbers of 2.5ms frames in "
                    "these cases."
                )
            frame_size: int = int(frame_duration * self._min_frame_samples)
        else:
            frame_size: int = PCM_BUFFER_SAMPLES

        len_data: int = len(data) if data is not None else 0

        with self._buf_lock:
            num_samples: int = self._decoder_fn(
                self._state,
                data,
                len_data,
                self._pcm,
                frame_size,
                1 if decode_fec else 0,
            )
            return list(self._pcm[0:num_samples])

    # Generic CTLs

    def reset_state(self) -> None:
        """
        Reset the decoder state.
        """
        ctl.decoder_reset_state(self._state)

    @property
    def final_range(self) -> int:
        """
        Get the final range of the decoder.

        Returns:
            int: Final range value.
        """
        return ctl.decoder_get_final_range(self._state)

    @property
    def pitch(self) -> int:
        """
        Get the pitch setting of the decoder.

        Returns:
            int: Pitch value.
        """
        return ctl.decoder_get_pitch(self._state)

    @property
    def bandwidth(self) -> int:
        """
        Get the bandwidth setting of the decoder.

        Returns:
            int: Bandwidth value.
        """
        return ctl.decoder_get_bandwidth(self._state)

    @property
    def gain(self) -> int:
        """
        Get the gain setting of the decoder.

        Returns:
            int: Gain value.
        """
        return ctl.decoder_get_gain(self._state)

    @gain.setter
    def gain(self, value: int) -> None:
        """
        Set the gain setting of the decoder.

        Args:
            value (int): Gain value to set.
        """
        ctl.decoder_set_gain(self._state, value)


class OpusDecoder(BaseOpusDecoder):
    """
    Opus decoder for integer PCM data.

    Inherits from BaseOpusDecoder and sets the decoding function to handle integer PCM data.
    """

    _buf_type: str = "int16_t[]"
    _decoder_fn: Callable[[Any, bytes, int, Any, int, int], int] = staticmethod(llinterface.decode)


class FloatOpusDecoder(BaseOpusDecoder):
    """
    Opus decoder for floating-point PCM data.

    Inherits from BaseOpusDecoder and sets the decoding function to handle floating-point PCM data.
    """

    _buf_type: str = "float[]"
    _decoder_fn: Callable[[Any, bytes, int, Any, int, int], int] = staticmethod(llinterface.decode_float)
