from typing import List

from flax import struct


@struct.dataclass
class EmptyState:
    pass


class StatefulObject:

    _instances: List["StatefulObject"] = []

    def __init__(self, n_visual_geoms: int =0):
        self.n_visual_geoms = n_visual_geoms
        self.visual_geoms_idx = None
        self._instances.append(self)

    def reset_state(self, env, model, data, carry, backend):
        return data, carry

    def init_state(self, env, key, model, data, backend):
        return EmptyState()

    @classmethod
    def get_all_instances(cls) -> List["MjvGeom"]:
        """Returns a list of all instances of this class."""
        return cls._instances
