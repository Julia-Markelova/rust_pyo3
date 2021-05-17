from dataclasses import dataclass
from typing import List
from uuid import UUID

from .model import FunctionalAreaType
from .model import Position
from .model import Rectangle


@dataclass
class ClusterOffsetRule:
    first_cluster_id: UUID
    second_cluster_id: UUID
    offset_m: float


@dataclass
class ClusterConnection:
    first_cluster_id: UUID
    second_cluster_id: UUID
    normalized_connection_cost: float


@dataclass
class BuildingWrapper:
    id: UUID
    figure: Rectangle
    local_position: Position
    label: str


@dataclass
class ClusterShape:
    cluster_id: UUID
    functional_area: FunctionalAreaType
    bounds: Rectangle
    buildings: List[BuildingWrapper]


@dataclass
class ClusterPosition:
    cluster_id: UUID
    offset_x_m: float
    offset_y_m: float
    angle_deg: float


@dataclass
class ClusterForce:
    cluster_id: UUID
    fx: float
    fy: float

    def __iadd__(self, other):
        if not isinstance(other, ClusterForce):
            raise TypeError
        if other.cluster_id != self.cluster_id:
            raise ValueError

        self.fx += other.fx
        self.fy += other.fy
        return self


@dataclass
class ClusterShift:
    cluster_id: UUID
    dx: float
    dy: float

    def __iadd__(self, other):
        if not isinstance(other, ClusterShift):
            raise TypeError
        if other.cluster_id != self.cluster_id:
            raise ValueError

        self.dx += other.dx
        self.dy += other.dy


@dataclass
class Force:
    building_id: UUID
    fx: float
    fy: float

    def __iadd__(self, other):
        if not isinstance(other, Force):
            raise TypeError
        if other.building_id != self.building_id:
            raise ValueError

        self.fx += other.fx
        self.fy += other.fy
        return self


@dataclass
class Direction:
    x: float
    y: float

    def __mul__(self, other):
        if not isinstance(other, float):
            raise TypeError()
        x = other * self.x
        y = other * self.y
        return Direction(
            x=x,
            y=y
        )

    def __rmul__(self, other):
        if not isinstance(other, float):
            raise TypeError()
        x = other * self.x
        y = other * self.y
        return Direction(
            x=x,
            y=y
        )

    def __add__(self, other):
        if not isinstance(other, Direction):
            raise TypeError()

        x = other.x + self.x
        y = other.y + self.y
        return Direction(
            x=x,
            y=y
        )


@dataclass
class Shift:
    building_id: UUID
    dx: float
    dy: float

    def __iadd__(self, other):
        if not isinstance(other, Shift):
            raise TypeError
        if other.building_id != self.building_id:
            raise ValueError

        self.dx += other.dx
        self.dy += other.dy
