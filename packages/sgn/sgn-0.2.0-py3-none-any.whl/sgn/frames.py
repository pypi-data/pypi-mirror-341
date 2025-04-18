"""Frame classes for the SGN framework."""

from dataclasses import dataclass, field
from typing import Any, Iterable

from sgn.base import Frame


@dataclass
class IterFrame(Frame):
    """A frame whose data attribute is an iterable.

    Args:
        data:
            Iterable, the data to store in the frame
    """

    data: Iterable[Any] = field(default_factory=list)
