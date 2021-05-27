from itertools import product
from math import sqrt
from typing import Dict
from typing import Tuple
from uuid import UUID

import numpy as np

from .internal import ClusterPosition
from .internal import ClusterShape
from .model import Position
from .model import Rectangle


def calculate_normalized_distance_between_two_clusters(
        first_cluster: ClusterShape,
        second_cluster: ClusterShape,
        first_cluster_position: ClusterPosition,
        second_cluster_position: ClusterPosition,
        building_offset_rules: Dict[Tuple[UUID, UUID], float]
) -> Tuple[float, float]:
    """
    Вычисление расстояния между кластерами с учётом оффсетов зданий. Возвращает минимальное значение из расстояний,
    разделённых на соответствующий оффсет.

    :return Tuple[float, float]: безразмерное расстояние, значение оффсета
   """
    first_building_positions = [
        _get_global_position_for_building(
            building.local_position,
            first_cluster_position
        )
        for building in first_cluster.buildings
    ]

    second_building_positions = [
        _get_global_position_for_building(
            building.local_position,
            second_cluster_position
        )
        for building in second_cluster.buildings
    ]

    first_building_figures = [building.figure for building in first_cluster.buildings]
    second_building_figures = [building.figure for building in second_cluster.buildings]
    first_building_id = [building.id for building in first_cluster.buildings]
    second_building_id = [building.id for building in second_cluster.buildings]

    distances = []
    offsets = []
    first_indices = list(range(len(first_cluster.buildings)))
    second_indices = list(range(len(second_cluster.buildings)))
    for first_idx, second_idx in product(first_indices, second_indices):
        first_figure, first_position = first_building_figures[first_idx], first_building_positions[first_idx]
        second_figure, second_position = second_building_figures[second_idx], second_building_positions[second_idx]
        offset_m = building_offset_rules[(first_building_id[first_idx], second_building_id[second_idx])]
        distances.append(calculate_distance_between_two_buildings(
            first_figure,
            second_figure,
            first_position,
            second_position
        ) / offset_m)
        offsets.append(offset_m)
    min_index = np.argmin(distances)
    return distances[min_index], offsets[min_index]


def calculate_distance_between_two_clusters(
        first_cluster: ClusterShape,
        second_cluster: ClusterShape,
        first_cluster_position: ClusterPosition,
        second_cluster_position: ClusterPosition
) -> float:
    first_building_positions = [
        _get_global_position_for_building(
            building.local_position,
            first_cluster_position
        )
        for building in first_cluster.buildings
    ]

    second_building_positions = [
        _get_global_position_for_building(
            building.local_position,
            second_cluster_position
        )
        for building in second_cluster.buildings
    ]

    first_building_figures = [building.figure for building in first_cluster.buildings]
    second_building_figures = [building.figure for building in second_cluster.buildings]

    distances = []
    first_indices = list(range(len(first_cluster.buildings)))
    second_indices = list(range(len(second_cluster.buildings)))
    for first_idx, second_idx in product(first_indices, second_indices):
        first_figure, first_position = first_building_figures[first_idx], first_building_positions[first_idx]
        second_figure, second_position = second_building_figures[second_idx], second_building_positions[second_idx]
        distances.append(
            calculate_distance_between_two_buildings(
                first_figure,
                second_figure,
                first_position,
                second_position
            )
        )

    return min(distances)


def calculate_distance_between_two_buildings(
        first_building_figure: Rectangle,
        second_building_figure: Rectangle,
        first_building_position: Position,
        second_building_position: Position
) -> float:
    delta_x = abs(first_building_position.offset_x_m - second_building_position.offset_x_m)
    delta_y = abs(first_building_position.offset_y_m - second_building_position.offset_y_m)
    total_half_width, total_half_length = _eval_half_total_width_and_half_total_length(
        first_figure=first_building_figure,
        second_figure=second_building_figure,
        first_angle_deg=first_building_position.angle_deg,
        second_angle_deg=second_building_position.angle_deg
    )

    if delta_x < total_half_length and delta_y >= total_half_width:
        return delta_y - total_half_width
    elif delta_x >= total_half_length and delta_y < total_half_width:
        return delta_x - total_half_length
    elif delta_x >= total_half_length and delta_y >= total_half_width:
        return sqrt((delta_x - total_half_length) ** 2 + (delta_y - total_half_width) ** 2)
    else:
        return -1.


def _get_global_position_for_building(
        local_position: Position,
        cluster_position: ClusterPosition
) -> Position:
    return Position(
        building_id=local_position.building_id,
        offset_x_m=local_position.offset_x_m + cluster_position.x,
        offset_y_m=local_position.offset_y_m + cluster_position.y,
        angle_deg=local_position.angle_deg
    )


def _eval_half_total_width_and_half_total_length(
        first_figure: Rectangle,
        second_figure: Rectangle,
        first_angle_deg: float,
        second_angle_deg: float
) -> Tuple[float, float]:
    first_length = first_figure.length_m / 2
    first_width = first_figure.width_m / 2
    # если угол поворота здания составляет 90 или 270 градусов
    # то длина является шириной, а ширина -- длиной
    if abs(first_angle_deg % 180 - 90) < 1e-5:
        first_length, first_width = first_width, first_length

    second_length = second_figure.length_m / 2
    second_width = second_figure.width_m / 2
    # если угол поворота здания составляет 90 или 270 градусов
    # то длина является шириной, а ширина -- длиной
    if abs(second_angle_deg % 180 - 90) < 1e-5:
        second_length, second_width = second_width, second_length

    return first_width + second_width, first_length + second_length
