use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

mod model;

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}

#[pyfunction]
fn calculate_distance_between_two_clusters(
    // создать структуру кластера, которая имплементит Copy и содержит Vec<Building> нельзя,
    // тк Vec в rust не имплементит Copy, поэтому такие аргументы
    first_cluster_buildings: Vec<model::Building>,
    second_cluster_buildings: Vec<model::Building>,
    first_cluster_position: model::Position,
    second_cluster_position: model::Position,
) -> f64 {
    let mut first_cluster_buildings = first_cluster_buildings.clone();
    let mut second_cluster_buildings = second_cluster_buildings.clone();

    // пересчитываем позиции сооружений с учетом положения кластера
    for building in &mut first_cluster_buildings {
        building.position = get_position_for_building(building.position, first_cluster_position)
    }
    for building in &mut second_cluster_buildings {
        building.position = get_position_for_building(building.position, second_cluster_position)
    }

    let mut distances: Vec<f64> = Vec::new();
    for first_building in first_cluster_buildings {
        for second_building in &second_cluster_buildings {
            distances.push(
                calculate_distance_between_two_buildings(first_building, *second_building)
            )
        }
    }

    let min = distances.iter().fold(f64::INFINITY, |a, &b| a.min(b));
    return min;
}

#[pyfunction]
fn calculate_distance_between_two_buildings(
    first_building: model::Building,
    second_building: model::Building,
) -> f64 {
    let delta_x: f64 = (first_building.position.offset_x_m - second_building.position.offset_x_m).abs();
    let delta_y: f64 = (first_building.position.offset_y_m - second_building.position.offset_y_m).abs();
    let (total_half_width, total_half_length): (f64, f64) = eval_half_total_width_and_half_total_length(
        first_building,
        second_building,
    );

    if delta_x < total_half_length && delta_y >= total_half_width {
        return delta_y - total_half_width;
    } else if delta_x >= total_half_length && delta_y < total_half_width {
        return delta_x - total_half_length;
    } else if delta_x >= total_half_length && delta_y >= total_half_width {
        return ((delta_x - total_half_length).powi(2) + (delta_y - total_half_width).powi(2)).sqrt();
    } else {
        return -1.;
    }
}


fn get_position_for_building(
    building_position: model::Position,
    cluster_position: model::Position,
) -> model::Position {
    let mut position;
    if (cluster_position.angle_deg).abs() < 1e-5 {  // 0
        position = model::Position {
            offset_x_m: building_position.offset_x_m,
            offset_y_m: building_position.offset_y_m,
            angle_deg: building_position.angle_deg,
        }
    } else if (cluster_position.angle_deg - 90.0).abs() < 1e-5 {  // 90
        position = model::Position {
            offset_x_m: building_position.offset_y_m,
            offset_y_m: -building_position.offset_x_m,
            angle_deg: building_position.angle_deg,
        }
    } else if (cluster_position.angle_deg - 180.0).abs() < 1e-5 {  // 180
        position = model::Position {
            offset_x_m: -building_position.offset_x_m,
            offset_y_m: -building_position.offset_y_m,
            angle_deg: building_position.angle_deg,
        }
    } else if (cluster_position.angle_deg - 270.0).abs() < 1e-5 {  // 270
        position = model::Position {
            offset_x_m: -building_position.offset_y_m,
            offset_y_m: building_position.offset_x_m,
            angle_deg: building_position.angle_deg,
        }
    } else {
        panic!("Unsupported angle value. Expected [0, 90, 180, 270]")
    }
    position.offset_x_m += cluster_position.offset_x_m;
    position.offset_y_m += cluster_position.offset_y_m;
    position.angle_deg = (position.angle_deg + cluster_position.angle_deg) % 360.0;
    return position;
}


fn eval_half_total_width_and_half_total_length(
    first_building: model::Building,
    second_building: model::Building,
) -> (f64, f64) {
    let first_length: f64 = first_building.rectangle.length_m / 2.0;
    let first_width: f64 = first_building.rectangle.width_m / 2.0;

    let (first_length, first_width): (f64, f64) = if (first_building.position.angle_deg % 180.0 - 90.0).abs() < 1e-5 {
        (first_width, first_length)
    } else {
        (first_length, first_width)
    };

    let second_length: f64 = second_building.rectangle.length_m / 2.0;
    let second_width: f64 = second_building.rectangle.width_m / 2.0;

    let (second_length, second_width): (f64, f64) = if (second_building.position.angle_deg % 180.0 - 90.0).abs() < 1e-5 {
        (second_width, second_length)
    } else {
        (second_length, second_width)
    };

    return (first_width + second_width, first_length + second_length);
}


/// A Python module implemented in Rust.
#[pymodule]
fn rust_force(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_distance_between_two_buildings, m)?)?;
    m.add_class::<model::Building>()?;
    m.add_class::<model::Position>()?;
    m.add_class::<model::Rectangle>()?;
    Ok(())
}