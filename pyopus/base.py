"""
This module provides internal classes for managing Opus codec states.

Classes:
    - ManagedState: Internal class for managing a chunk of memory storing codec state.
    - OpusCodec: Base class for Opus encoder and decoder.
"""

from typing import Any
from .binding import ffi


__all__: list[str] = [
    "ManagedState",
    "OpusCodec",
]


class ManagedState:
    """
    Internal class for managing a chunk of memory storing codec state.

    Attributes:
        _state (Any): The allocated memory buffer for codec state.
    """

    def __init__(self) -> None:
        """
        Initialize the ManagedState by allocating memory and initializing the codec state.

        Raises:
            NotImplementedError: If `_get_state_size` or `_init_state` are not implemented in subclasses.
        """
        state_size: int = self._get_state_size()
        self._state: Any = ffi.new("char[]", state_size)
        self._init_state()

    def _get_state_size(self) -> int:
        """
        Retrieve the size of the codec state in bytes.

        This method should be implemented by subclasses to specify the required state size.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError("Subclasses must implement `_get_state_size` method.")

    def _init_state(self) -> None:
        """
        Initialize the codec state.

        This method should be implemented by subclasses to perform state-specific initialization.

        Raises:
            NotImplementedError: If not implemented in the subclass.
        """
        raise NotImplementedError("Subclasses must implement `_init_state` method.")


class OpusCodec(ManagedState):
    """
    Base class for Opus encoder and decoder.

    Inherits from `ManagedState` and provides a foundation for specific codec implementations.
    """

    def __init__(self) -> None:
        """
        Initialize the OpusCodec by calling the parent class initializer.
        """
        super().__init__()
