import random

import rust_force

from force.model import Position
from force.model import Rectangle
from force.distance import calculate_distance_between_two_buildings

building_count = 10

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


rust_buildings = [
    rust_force.Building(
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


def test_result():
    rust_result = rust_force.calculate_distance_between_two_buildings(rust_buildings[0], rust_buildings[1])
    python_result = calculate_distance_between_two_buildings(
        python_figures[0], python_figures[1], python_positions[0], python_positions[1])
    assert rust_result == python_result


def test_python(benchmark):
    benchmark(calculate_distance_between_two_buildings,
              python_figures[0], python_figures[1], python_positions[0], python_positions[1])


def test_rust(benchmark):
    benchmark(rust_force.calculate_distance_between_two_buildings, rust_buildings[0], rust_buildings[1])
