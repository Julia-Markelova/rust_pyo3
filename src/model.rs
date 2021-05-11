use pyo3::prelude::*;

#[pyclass]
#[derive(Copy, Clone)]
pub struct Rectangle {
    pub width_m: f64,
    pub length_m: f64,
}

#[pyclass]
#[derive(Copy, Clone)]
pub struct Position {
    pub offset_x_m: f64,
    pub offset_y_m: f64,
    pub angle_deg: f64,
}


#[pyclass]
#[derive(Copy, Clone)]
pub struct Building {
    pub rectangle: Rectangle,
    pub position: Position,
}


#[pymethods]
impl Rectangle {
    #[new]
    fn new(width_m: f64, length_m: f64) -> Self {
        Rectangle { width_m, length_m }
    }

    #[getter]
    fn width_m(&self) -> PyResult<f64> {
        Ok(self.width_m)
    }

    #[getter]
    fn length_m(&self) -> PyResult<f64> {
        Ok(self.length_m)
    }
}


#[pymethods]
impl Position {
    #[new]
    fn new(offset_x_m: f64, offset_y_m: f64, angle_deg: f64) -> Self {
        Position { offset_x_m, offset_y_m, angle_deg }
    }

    #[getter]
    fn offset_x_m(&self) -> PyResult<f64> {
        Ok(self.offset_x_m)
    }

    #[getter]
    fn offset_y_m(&self) -> PyResult<f64> {
        Ok(self.offset_y_m)
    }

    #[getter]
    fn angle_deg(&self) -> PyResult<f64> {
        Ok(self.angle_deg)
    }
}


#[pymethods]
impl Building {
    #[new]
    fn new(rectangle: Rectangle, position: Position) -> Self {
        Building { rectangle, position }
    }

    #[getter]
    fn rectangle(&self) -> PyResult<Rectangle> {
        Ok(self.rectangle)
    }

    #[getter]
    fn position(&self) -> PyResult<Position> {
        Ok(self.position)
    }
}

