from . import constants
from typing import Final

__all__: list[str] = [
    "check_freq",
    "check_channels",
    "check_application",
]

_SUPPORTED_FREQS: Final[frozenset[int]] = frozenset({8000, 12000, 16000, 24000, 48000})
_SUPPORTED_CHANNELS: Final[frozenset[int]] = frozenset({1, 2})
_SUPPORTED_APPLICATIONS: Final[frozenset[int]] = frozenset({
    constants.APPLICATION_VOIP,
    constants.APPLICATION_AUDIO,
    constants.APPLICATION_RESTRICTED_LOWDELAY,
})


def check_freq(frequency: int) -> None:
    """
    Validate if the provided frequency is supported.

    Args:
        frequency (int): The frequency to validate.

    Raises:
        ValueError: If the frequency is not supported. The error message includes the list of supported frequencies.
    """
    if frequency not in _SUPPORTED_FREQS:
        supported = sorted(_SUPPORTED_FREQS)
        raise ValueError(f"Unsupported frequency; please use one of {supported!r}")


def check_channels(channels: int) -> None:
    """
    Validate if the provided number of channels is supported.

    Args:
        channels (int): The number of channels to validate.

    Raises:
        ValueError: If the number of channels is not supported. Only 1 or 2 channels are allowed.
    """
    if channels not in _SUPPORTED_CHANNELS:
        raise ValueError("Unsupported number of channels; only 1 or 2 are supported")


def check_application(application: int) -> None:
    """
    Validate if the provided application coding mode is supported.

    Args:
        application (int): The application coding mode to validate.

    Raises:
        ValueError: If the application coding mode is not supported. The error message suggests consulting Opus documentation for proper constants.
    """
    if application not in _SUPPORTED_APPLICATIONS:
        raise ValueError(
            "Unsupported coding mode; please consult Opus docs for the proper constant to use"
        )
