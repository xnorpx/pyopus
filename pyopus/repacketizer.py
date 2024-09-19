from typing import Final

from . import base, llinterface

__all__: list[str] = [
    "OpusRepacketizer",
]


class OpusRepacketizer(base.ManagedState):
    """Opus repacketizer."""

    def __init__(self) -> None:
        """Initialize the Opus repacketizer state."""
        super().__init__()

    def _get_state_size(self) -> int:
        """
        Retrieve the size of the repacketizer state.

        Returns:
            int: The size of the repacketizer state.
        """
        return llinterface.repacketizer_get_size()

    def _init_state(self) -> None:
        """
        Initialize the repacketizer state.

        Raises:
            SomeException: If initialization fails (modify as appropriate).
        """
        llinterface.repacketizer_init(self._state)
