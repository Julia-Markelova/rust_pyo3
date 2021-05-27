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
pub struct ClusterPosition {
    pub x: f64,
    pub y: f64,
}

#[pyclass]
#[derive(Copy, Clone)]
pub struct Building {
    // в расте используем uuid, а в питоне - строки
    // в расте со строками нельзя имплементить Copy
    // для питона нет (я пока не нашла) аналога для uuid
    pub id: uuid::Uuid,
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
impl ClusterPosition {
    #[new]
    fn new(x: f64, y: f64, ) -> Self {
        ClusterPosition { x, y }
    }

    #[getter]
    fn x(&self) -> PyResult<f64> {
        Ok(self.x)
    }

    #[getter]
    fn y(&self) -> PyResult<f64> {
        Ok(self.y)
    }

}


#[pymethods]
impl Building {
    #[new]
    fn new(id: String, rectangle: Rectangle, position: Position) -> Self {
        Building {
            id: uuid::Uuid::parse_str(&id).unwrap(),
            rectangle,
            position }
    }

    #[getter]
    fn id(&self) -> PyResult<String> {
        Ok(self.id.to_string())
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

