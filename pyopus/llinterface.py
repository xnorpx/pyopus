"""
This module provides Python bindings for the Opus codec library using cffi.
It includes functions for encoding and decoding audio, managing Opus encoders and decoders,
handling errors, and manipulating Opus packets and repacketizers.

Functions:
    - strerror: Retrieve a human-readable error message for a given Opus error code.
    - get_version_string: Get the Opus library version string.
    - encoder_get_size: Get the size of an Opus encoder state.
    - encoder_create: Create a new Opus encoder.
    - encoder_init: Initialize an existing Opus encoder.
    - encode: Encode PCM data into Opus.
    - encode_float: Encode floating-point PCM data into Opus.
    - encoder_destroy: Destroy an Opus encoder.
    - encoder_ctl: Control operations on an Opus encoder.
    - decoder_get_size: Get the size of an Opus decoder state.
    - decoder_create: Create a new Opus decoder.
    - decoder_init: Initialize an existing Opus decoder.
    - decode: Decode Opus data into PCM.
    - decode_float: Decode Opus data into floating-point PCM.
    - decoder_ctl: Control operations on an Opus decoder.
    - decoder_destroy: Destroy an Opus decoder.
    - packet_get_bandwidth: Retrieve the bandwidth of an Opus packet.
    - packet_get_samples_per_frame: Get the number of samples per frame in an Opus packet.
    - packet_get_nb_channels: Get the number of channels in an Opus packet.
    - packet_get_nb_frames: Get the number of frames in an Opus packet.
    - packet_get_nb_samples: Get the number of samples in an Opus packet.
    - decoder_get_nb_samples: Get the number of samples produced by a decoder for a given packet.
    - pcm_soft_clip: Apply soft clipping to PCM data.
    - repacketizer_get_size: Get the size of an Opus repacketizer state.
    - repacketizer_init: Initialize an existing Opus repacketizer.
    - repacketizer_create: Create a new Opus repacketizer.
    - repacketizer_destroy: Destroy an Opus repacketizer.
"""

from enum import Enum
from typing import Any, List, Optional, Union

from .binding import C, ffi
from .constants import OK, OPUS_INVALID_PACKET  # Assuming OPUS_INVALID_PACKET exists


__all__: list[str] = [
    "strerror",
    "get_version_string",
    "encoder_get_size",
    "encoder_create",
    "encoder_init",
    "encode",
    "encode_float",
    "encoder_destroy",
    "encoder_ctl",
    "decoder_get_size",
    "decoder_create",
    "decoder_init",
    "decode",
    "decode_float",
    "decoder_ctl",
    "decoder_destroy",
    "packet_get_bandwidth",
    "packet_get_samples_per_frame",
    "packet_get_nb_channels",
    "packet_get_nb_frames",
    "packet_get_nb_samples",
    "decoder_get_nb_samples",
    "pcm_soft_clip",
    "repacketizer_get_size",
    "repacketizer_init",
    "repacketizer_create",
    "repacketizer_destroy",
]


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
        msg = strerror(errno)
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


def strerror(error: int) -> str:
    """
    Retrieve a human-readable error message for a given Opus error code.

    Args:
        error (int): The Opus error code.

    Returns:
        str: A descriptive error message.
    """
    return ffi.string(C.opus_strerror(error)).decode("utf-8")


def get_version_string() -> str:
    """
    Get the Opus library version string.

    Returns:
        str: The version string of the Opus library.
    """
    return ffi.string(C.opus_get_version_string()).decode("utf-8")


def encoder_get_size(channels: int) -> int:
    """
    Get the size of an Opus encoder state for a given number of channels.

    Args:
        channels (int): The number of audio channels.

    Returns:
        int: The size in bytes of the Opus encoder state.
    """
    return C.opus_encoder_get_size(channels)


class OpusApplication(Enum):
    VOIP = 2048  # Replace with actual constant value from constants.APPLICATION_VOIP
    AUDIO = 2049  # Replace with actual constant value from constants.APPLICATION_AUDIO
    RESTRICTED_LOWDELAY = 2051  # Replace with actual constant value from constants.APPLICATION_RESTRICTED_LOWDELAY


def encoder_create(Fs: int, channels: int, application: OpusApplication) -> Any:
    """
    Create a new Opus encoder.

    Args:
        Fs (int): Sampling rate (Hz).
        channels (int): Number of audio channels.
        application (OpusApplication): The encoding application (e.g., VOIP, AUDIO).

    Returns:
        Any: A pointer to the newly created OpusEncoder.

    Raises:
        OpusError: If the encoder creation fails.
    """
    error_p = ffi.new("int[1]")
    st = C.opus_encoder_create(Fs, channels, application.value, error_p)
    error = error_p[0]

    if error != OK:
        raise OpusError(error)

    return st


def encoder_init(st: Any, Fs: int, channels: int, application: OpusApplication) -> None:
    """
    Initialize an existing Opus encoder.

    Args:
        st (Any): The OpusEncoder to initialize.
        Fs (int): Sampling rate (Hz).
        channels (int): Number of audio channels.
        application (OpusApplication): The encoding application.

    Raises:
        OpusError: If the encoder initialization fails.
    """
    error = C.opus_encoder_init(st, Fs, channels, application.value)

    if error != OK:
        raise OpusError(error)


def encode(
    st: Any,
    pcm: bytes,
    frame_size: int,
    data: bytes,
    max_data_bytes: int
) -> int:
    """
    Encode PCM data into Opus format.

    Args:
        st (Any): The OpusEncoder.
        pcm (bytes): PCM audio data (int16).
        frame_size (int): Number of samples per channel.
        data (bytes): Buffer to store encoded Opus data.
        max_data_bytes (int): Maximum number of bytes that can be written to 'data'.

    Returns:
        int: Number of bytes written to 'data'.

    Raises:
        OpusError: If encoding fails.
    """
    result = C.opus_encode(st, pcm, frame_size, data, max_data_bytes)

    if result < 0:
        raise OpusError(result)

    return result


def encode_float(
    st: Any,
    pcm: bytes,
    frame_size: int,
    data: bytes,
    max_data_bytes: int
) -> int:
    """
    Encode floating-point PCM data into Opus format.

    Args:
        st (Any): The OpusEncoder.
        pcm (bytes): PCM audio data (float).
        frame_size (int): Number of samples per channel.
        data (bytes): Buffer to store encoded Opus data.
        max_data_bytes (int): Maximum number of bytes that can be written to 'data'.

    Returns:
        int: Number of bytes written to 'data'.

    Raises:
        OpusError: If encoding fails.
    """
    result = C.opus_encode_float(st, pcm, frame_size, data, max_data_bytes)

    if result < 0:
        raise OpusError(result)

    return result


def encoder_destroy(st: Any) -> None:
    """
    Destroy an Opus encoder and free its resources.

    Args:
        st (Any): The OpusEncoder to destroy.
    """
    C.opus_encoder_destroy(st)


def encoder_ctl(st: Any, request: int, *args: Any) -> None:
    """
    Control operations on an Opus encoder.

    Args:
        st (Any): The OpusEncoder.
        request (int): The control request code.
        *args (Any): Additional arguments for the control request.

    Raises:
        OpusError: If the control operation fails.
    """
    error = C.opus_encoder_ctl(st, request, *args)

    if error != OK:
        raise OpusError(error)


def decoder_get_size(channels: int) -> int:
    """
    Get the size of an Opus decoder state for a given number of channels.

    Args:
        channels (int): Number of audio channels.

    Returns:
        int: The size in bytes of the Opus decoder state.
    """
    return C.opus_decoder_get_size(channels)


def decoder_create(Fs: int, channels: int) -> Any:
    """
    Create a new Opus decoder.

    Args:
        Fs (int): Sampling rate (Hz).
        channels (int): Number of audio channels.

    Returns:
        Any: A pointer to the newly created OpusDecoder.

    Raises:
        OpusError: If the decoder creation fails.
    """
    error_p = ffi.new("int[1]")
    st = C.opus_decoder_create(Fs, channels, error_p)
    error = error_p[0]

    if error != OK:
        raise OpusError(error)

    return st


def decoder_init(st: Any, Fs: int, channels: int) -> None:
    """
    Initialize an existing Opus decoder.

    Args:
        st (Any): The OpusDecoder to initialize.
        Fs (int): Sampling rate (Hz).
        channels (int): Number of audio channels.

    Raises:
        OpusError: If the decoder initialization fails.
    """
    error = C.opus_decoder_init(st, Fs, channels)

    if error != OK:
        raise OpusError(error)


def decode(
    st: Any,
    data: bytes,
    length: int,
    pcm: bytes,
    frame_size: int,
    decode_fec: int
) -> int:
    """
    Decode Opus data into PCM format.

    Args:
        st (Any): The OpusDecoder.
        data (bytes): Encoded Opus data.
        length (int): Number of bytes in 'data'.
        pcm (bytes): Buffer to store decoded PCM data (int16).
        frame_size (int): Number of samples per channel.
        decode_fec (int): Decode in-band forward error correction.

    Returns:
        int: Number of samples decoded per channel.

    Raises:
        OpusError: If decoding fails.
    """
    result = C.opus_decode(st, data, length, pcm, frame_size, decode_fec)

    if result < 0:
        raise OpusError(result)

    return result


def decode_float(
    st: Any,
    data: bytes,
    length: int,
    pcm: bytes,
    frame_size: int,
    decode_fec: int
) -> int:
    """
    Decode Opus data into floating-point PCM format.

    Args:
        st (Any): The OpusDecoder.
        data (bytes): Encoded Opus data.
        length (int): Number of bytes in 'data'.
        pcm (bytes): Buffer to store decoded PCM data (float).
        frame_size (int): Number of samples per channel.
        decode_fec (int): Decode in-band forward error correction.

    Returns:
        int: Number of samples decoded per channel.

    Raises:
        OpusError: If decoding fails.
    """
    result = C.opus_decode_float(st, data, length, pcm, frame_size, decode_fec)

    if result < 0:
        raise OpusError(result)

    return result


def decoder_ctl(st: Any, request: int, *args: Any) -> None:
    """
    Control operations on an Opus decoder.

    Args:
        st (Any): The OpusDecoder.
        request (int): The control request code.
        *args (Any): Additional arguments for the control request.

    Raises:
        OpusError: If the control operation fails.
    """
    error = C.opus_decoder_ctl(st, request, *args)

    if error != OK:
        raise OpusError(error)


def decoder_destroy(st: Any) -> None:
    """
    Destroy an Opus decoder and free its resources.

    Args:
        st (Any): The OpusDecoder to destroy.
    """
    C.opus_decoder_destroy(st)


def packet_get_bandwidth(data: bytes) -> int:
    """
    Retrieve the bandwidth of an Opus packet.

    Args:
        data (bytes): Encoded Opus packet.

    Returns:
        int: The bandwidth of the packet.

    Raises:
        OpusError: If the packet is invalid.
    """
    result = C.opus_packet_get_bandwidth(data)

    if result < 0:
        raise OpusError(result)

    return result


def packet_get_samples_per_frame(data: bytes, Fs: int) -> int:
    """
    Get the number of samples per frame in an Opus packet.

    Args:
        data (bytes): Encoded Opus packet.
        Fs (int): Sampling rate (Hz).

    Returns:
        int: Number of samples per frame.

    Raises:
        OpusError: If the packet is invalid.
    """
    result = C.opus_packet_get_samples_per_frame(data, Fs)

    if result < 0:
        raise OpusError(result)

    return result


def packet_get_nb_channels(data: bytes) -> int:
    """
    Get the number of channels in an Opus packet.

    Args:
        data (bytes): Encoded Opus packet.

    Returns:
        int: Number of audio channels.

    Raises:
        OpusError: If the packet is invalid.
    """
    result = C.opus_packet_get_nb_channels(data)

    if result < 0:
        raise OpusError(result)

    return result


def packet_get_nb_frames(packet: bytes, length: int) -> int:
    """
    Get the number of frames in an Opus packet.

    Args:
        packet (bytes): Encoded Opus packet.
        length (int): Number of bytes in 'packet'.

    Returns:
        int: Number of frames in the packet.

    Raises:
        OpusError: If the packet is invalid.
    """
    result = C.opus_packet_get_nb_frames(packet, length)

    if result < 0:
        raise OpusError(result)

    return result


def packet_get_nb_samples(packet: bytes, length: int, Fs: int) -> int:
    """
    Get the number of samples in an Opus packet.

    Args:
        packet (bytes): Encoded Opus packet.
        length (int): Number of bytes in 'packet'.
        Fs (int): Sampling rate (Hz).

    Returns:
        int: Number of samples in the packet.

    Raises:
        OpusError: If the packet is invalid.
    """
    result = C.opus_packet_get_nb_samples(packet, length, Fs)

    if result < 0:
        raise OpusError(result)

    return result


def decoder_get_nb_samples(dec: Any, packet: bytes, length: int) -> int:
    """
    Get the number of samples produced by a decoder for a given packet.

    Args:
        dec (Any): The OpusDecoder.
        packet (bytes): Encoded Opus packet.
        length (int): Number of bytes in 'packet'.

    Returns:
        int: Number of samples decoded.

    Raises:
        OpusError: If the packet is invalid.
    """
    result = C.opus_decoder_get_nb_samples(dec, packet, length)

    if result < 0:
        raise OpusError(result)

    return result


def pcm_soft_clip(
    pcm: bytes,
    frame_size: int,
    channels: int,
    softclip_mem: bytes
) -> None:
    """
    Apply soft clipping to PCM data to prevent clipping.

    Args:
        pcm (bytes): PCM audio data (float).
        frame_size (int): Number of samples per channel.
        channels (int): Number of audio channels.
        softclip_mem (bytes): Memory buffer for soft clipping state.
    """
    C.opus_pcm_soft_clip(pcm, frame_size, channels, softclip_mem)


def repacketizer_get_size() -> int:
    """
    Get the size of an Opus repacketizer state.

    Returns:
        int: The size in bytes of the Opus repacketizer state.
    """
    return C.opus_repacketizer_get_size()


def repacketizer_init(rp: Any) -> Any:
    """
    Initialize an existing Opus repacketizer.

    Args:
        rp (Any): The OpusRepacketizer to initialize.

    Returns:
        Any: The initialized OpusRepacketizer.

    Raises:
        OpusError: If initialization fails.
    """
    result = C.opus_repacketizer_init(rp)

    if result is None:
        raise OpusError(OPUS_INVALID_PACKET)

    return result


def repacketizer_create() -> Any:
    """
    Create a new Opus repacketizer.

    Returns:
        Any: A pointer to the newly created OpusRepacketizer.

    Raises:
        OpusError: If the repacketizer creation fails.
    """
    rp = C.opus_repacketizer_create()

    if rp is None:
        raise OpusError(OPUS_INVALID_PACKET)

    return rp


def repacketizer_destroy(rp: Any) -> None:
    """
    Destroy an Opus repacketizer and free its resources.

    Args:
        rp (Any): The OpusRepacketizer to destroy.
    """
    C.opus_repacketizer_destroy(rp)
