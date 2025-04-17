use pyo3::prelude::*;
use pyo3::types::PyList;

#[pyclass(frozen)]
// FIXME: this is copy&paste from the original crate.
// It's needed as pyclass cannot be applied over external enums
enum TrackerStatus {
    Unborn,
    Born,
    Alive,
    Dead,
    Zombie,
}

#[pyclass(frozen)]
struct TrackingResult(::track_sort::TrackingResult);

#[pymethods]
impl TrackingResult {
    #[getter]
    fn status(&self) -> TrackerStatus {
        match self.0.status {
            ::track_sort::TrackerStatus::Unborn => TrackerStatus::Unborn,
            ::track_sort::TrackerStatus::Born => TrackerStatus::Born,
            ::track_sort::TrackerStatus::Alive => TrackerStatus::Alive,
            ::track_sort::TrackerStatus::Dead => TrackerStatus::Dead,
            ::track_sort::TrackerStatus::Zombie => TrackerStatus::Zombie,
        }
    }

    #[getter]
    fn tracker_id(&self) -> u64 {
        self.0.tracker_id
    }

    #[getter]
    fn detection_box(&self) -> DetectionBox {
        DetectionBox::new(
            self.0.detection_box.x,
            self.0.detection_box.y,
            self.0.detection_box.w,
            self.0.detection_box.h,
        )
    }

    #[getter]
    fn age(&self) -> u32 {
        self.0.age
    }

    #[getter]
    fn time_since_update(&self) -> u64 {
        self.0.time_since_update
    }

    #[getter]
    fn hit_streak(&self) -> u32 {
        self.0.hit_streak
    }

    #[getter]
    fn hits(&self) -> u32 {
        self.0.hits
    }
}

#[pyclass(frozen)]
#[derive(Clone)]
struct DetectionBox(::track_sort::Box);

#[pymethods]
impl DetectionBox {
    #[new]
    #[pyo3(signature = (x=0., y=0., w=0., h=0.))]
    fn new(x: f32, y: f32, w: f32, h: f32) -> Self {
        Self(::track_sort::Box { x, y, w, h })
    }

    #[getter]
    fn x(&self) -> f32 {
        self.0.x
    }

    #[getter]
    fn y(&self) -> f32 {
        self.0.y
    }

    #[getter]
    fn w(&self) -> f32 {
        self.0.w
    }
    #[getter]
    fn h(&self) -> f32 {
        self.0.h
    }
}

#[pyclass]
struct Tracker {
    tracker: ::track_sort::Tracker,
    config: ::track_sort::Config,
}

#[pymethods]
impl Tracker {
    #[new]
    #[pyo3(signature = (threshold=0.3, min_hits=3, max_age=1))]
    fn new(threshold: f32, min_hits: u32, max_age: u64) -> Self {
        Self {
            tracker: ::track_sort::Tracker::default(),
            config: ::track_sort::Config {
                iou_threshold: threshold,
                min_hits,
                max_age,
            },
        }
    }

    fn update<'p>(
        &mut self,
        py: Python<'p>,
        boxes: Vec<DetectionBox>,
    ) -> PyResult<Bound<'p, PyList>> {
        let b = boxes
            .iter()
            .map(|b| b.0)
            .collect::<Vec<::track_sort::Box>>();

        let r = self.tracker.track_boxes(&self.config, b.as_slice());
        PyList::new(py, r.iter().map(|r| TrackingResult(*r)))
    }
}

#[pymodule]
fn track_sort(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Tracker>()?;
    m.add_class::<TrackingResult>()?;
    m.add_class::<DetectionBox>()?;
    m.add_class::<TrackerStatus>()?;
    Ok(())
}
