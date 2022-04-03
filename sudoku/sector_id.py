from enum import auto, Enum
from typing import Tuple


class SectorId(Enum):
    TopLeft = auto()
    Top = auto()
    TopRight = auto()
    CenterLeft = auto()
    Center = auto()
    CenterRight = auto()
    BottomLeft = auto()
    Bottom = auto()
    BottomRight = auto()

    @staticmethod
    def get_starting_indices(sector: "SectorId") -> Tuple[int, int]:
        indices = {
            SectorId.TopLeft: (0, 0),
            SectorId.Top: (0, 3),
            SectorId.TopRight: (0, 6),
            SectorId.CenterLeft: (3, 0),
            SectorId.Center: (3, 3),
            SectorId.CenterRight: (3, 6),
            SectorId.BottomLeft: (6, 0),
            SectorId.Bottom: (6, 3),
            SectorId.BottomRight: (6, 6)
        }
        return indices.get(sector)
