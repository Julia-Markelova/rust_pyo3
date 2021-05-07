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
fn rust_force(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(calculate_distance_between_two_buildings, m)?)?;
    m.add_class::<model::Building>()?;
    m.add_class::<model::Position>()?;
    m.add_class::<model::Rectangle>()?;
    Ok(())
}