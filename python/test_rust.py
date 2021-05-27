import json
import random
from itertools import product
from typing import Dict, Tuple
from uuid import UUID
from uuid import uuid4

import rust_force

from force.distance import calculate_distance_between_two_buildings, calculate_distance_between_two_clusters
from force.distance import calculate_normalized_distance_between_two_clusters
from force.internal import BuildingWrapper
from force.internal import ClusterPosition
from force.internal import ClusterShape
from force.model import FunctionalAreaType
from force.model import Position
from force.model import Rectangle

building_count = 12
n_first_cluster = 5

first_cluster_id = UUID('10000000-0000-0000-0000-000000000000')
second_cluster_id = UUID('20000000-0000-0000-0000-000000000000')

python_positions = [
    Position(
        offset_x_m=random.randint(0, 100),
        offset_y_m=random.randint(0, 100),
        angle_deg=random.choice([0, 90, 180, 270])
    )
    for i in range(building_count)
]

python_figures = [
    Rectangle(
        width_m=random.randint(5, 100),
        length_m=random.randint(5, 100),
    )
    for i in range(building_count)
]

python_buildings = [BuildingWrapper(
    id=uuid4(),
    label='',
    local_position=python_positions[i],
    figure=python_figures[i],
    connection_points=[])
    for i in range(building_count)]

rust_buildings = [
    rust_force.Building(
        id=str(python_buildings[i].id),
        rectangle=rust_force.Rectangle(
            width_m=python_figures[i].width_m,
            length_m=python_figures[i].length_m,
        ),
        position=rust_force.Position(
            offset_x_m=python_positions[i].offset_x_m,
            offset_y_m=python_positions[i].offset_y_m,
            angle_deg=python_positions[i].angle_deg
        )
    )
    for i in range(building_count)
]

rust_first_cluster_position = rust_force.ClusterPosition(x=random.randint(0, 100),
                                                         y=random.randint(0, 100))

rust_second_cluster_position = rust_force.ClusterPosition(x=random.randint(0, 100),
                                                          y=random.randint(0, 100))

python_first_cluster = ClusterShape(
    cluster_id=first_cluster_id,
    buildings=python_buildings[:n_first_cluster],
    functional_area=FunctionalAreaType.ONE,
    figure=python_figures[0]
)

python_second_cluster = ClusterShape(
    cluster_id=second_cluster_id,
    buildings=python_buildings[n_first_cluster:],
    functional_area=FunctionalAreaType.ONE,
    figure=python_figures[0]
)

python_first_cluster_position = ClusterPosition(cluster_id=first_cluster_id,
                                                x=rust_first_cluster_position.x,
                                                y=rust_first_cluster_position.y)
python_second_cluster_position = ClusterPosition(cluster_id=second_cluster_id,
                                                 x=rust_second_cluster_position.x,
                                                 y=rust_second_cluster_position.y)

building_offset_rules: Dict[Tuple[UUID, UUID], float] = {}
rust_building_offset_rules: Dict[Tuple[str, str], float] = {}
for b1, b2 in product(python_buildings, python_buildings):
    if b1.id != b2.id:
        offset = random.randint(1, 100)
        building_offset_rules[(b1.id, b2.id)] = offset
        building_offset_rules[(b2.id, b1.id)] = offset
        rust_building_offset_rules[f'{b1.id}_{b2.id}'] = offset
        rust_building_offset_rules[f'{b2.id}_{b1.id}'] = offset

with open('offsets.json', 'w') as file:
    json.dump(rust_building_offset_rules, file)


def test_equals_normalized_distance_clusters():
    """
    check for equals normalized distance between clusters in python and rust
    """
    rust_result = rust_force.calculate_normalized_distance_between_two_clusters(
        rust_buildings[:n_first_cluster], rust_buildings[n_first_cluster:], rust_first_cluster_position,
        rust_second_cluster_position)
    python_result = calculate_normalized_distance_between_two_clusters(
        python_first_cluster, python_second_cluster, python_first_cluster_position, python_second_cluster_position,
        building_offset_rules)
    assert rust_result == python_result


def test_equals_distance_buildings():
    """
    check for equals distance between buildings in python and rust
    """
    for i in range(building_count):
        for j in range(building_count):
            if i == j:
                continue
            rust_result = rust_force.calculate_distance_between_two_buildings(
                rust_buildings[i], rust_buildings[j])
            python_result = calculate_distance_between_two_buildings(
                python_figures[i], python_figures[j], python_positions[i], python_positions[j])
            assert rust_result == python_result


def test_equals_distance_clusters():
    """
    check for equals distance between clusters in python and rust
    """
    rust_result = rust_force.calculate_distance_between_two_clusters(
        rust_buildings[:n_first_cluster], rust_buildings[n_first_cluster:], rust_first_cluster_position,
        rust_second_cluster_position)
    python_result = calculate_distance_between_two_clusters(
        python_first_cluster, python_second_cluster, python_first_cluster_position, python_second_cluster_position)
    assert rust_result == python_result


def test_equals_distance_clusters_rust():
    """
    check for equals distance between clusters in parallel rust and rust
    """
    rust_result = rust_force.calculate_distance_between_two_clusters(
        rust_buildings[:n_first_cluster], rust_buildings[n_first_cluster:], rust_first_cluster_position,
        rust_second_cluster_position)
    rust_result_parallel = rust_force.calculate_distance_between_two_clusters_parallel(
        rust_buildings[:n_first_cluster], rust_buildings[n_first_cluster:], rust_first_cluster_position,
        rust_second_cluster_position)
    assert rust_result == rust_result_parallel


# benchmarks
def test_distance_clusters_python(benchmark):
    benchmark(calculate_distance_between_two_clusters,
              python_first_cluster, python_second_cluster,
              python_first_cluster_position, python_second_cluster_position)


def test_distance_clusters_rust(benchmark):
    benchmark(rust_force.calculate_distance_between_two_clusters, rust_buildings[:n_first_cluster],
              rust_buildings[n_first_cluster:],
              rust_first_cluster_position, rust_second_cluster_position)


def test_distance_clusters_rust_parallel(benchmark):
    benchmark(rust_force.calculate_distance_between_two_clusters_parallel, rust_buildings[:n_first_cluster],
              rust_buildings[n_first_cluster:],
              rust_first_cluster_position, rust_second_cluster_position)
