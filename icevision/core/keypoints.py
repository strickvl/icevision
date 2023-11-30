__all__ = ["KeyPoints", "KeypointConnection", "KeypointsMetadata"]

from icevision.imports import *
from .exceptions import *


class KeypointConnection:
    def __init__(self, p1, p2, color=None):
        self.p1 = p1
        self.p2 = p2
        self.color = color or (100, 100, 100)


class KeypointsMetadata:
    labels: Tuple[str] = NotImplemented
    connections: Tuple[KeypointConnection] = None


class KeyPoints:
    def __init__(
        self, keypoints: Union[List[int], np.array], metadata: Type[KeypointsMetadata]
    ):
        self.keypoints = np.array(keypoints)
        self.x = self.keypoints[::3]
        self.y = self.keypoints[1::3]
        self.visible = self.keypoints[2::3]
        self.xy = list(zip(self.x, self.y))
        self.n_visible_keypoints = (self.visible > 0).sum()
        self.xyv = list(zip(self.x, self.y, self.visible))
        self.metadata = metadata

    @classmethod
    def from_xyv(cls, keypoints, labels):
        return cls(keypoints, labels)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"({self.n_visible_keypoints} visible keypoints)>"
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, KeyPoints):
            return (
                np.all(self.keypoints == other.keypoints)
                and self.metadata == other.metadata
            )
        return False
