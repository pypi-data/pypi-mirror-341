use crate::core;
use pyo3::{prelude::*, types::PyList, IntoPyObjectExt};

#[derive(Debug)]
enum EditDistanceItem {
    String(String),
    Int(i64),
    Float(f64),
    Bool(bool),
    Object(Py<PyAny>),
}

impl PartialEq for EditDistanceItem {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (EditDistanceItem::String(a), EditDistanceItem::String(b)) => a == b,
            (EditDistanceItem::Int(a), EditDistanceItem::Int(b)) => a == b,
            (EditDistanceItem::Float(a), EditDistanceItem::Float(b)) => a == b,
            (EditDistanceItem::Bool(a), EditDistanceItem::Bool(b)) => a == b,
            (EditDistanceItem::Object(a), EditDistanceItem::Object(b)) => {
                // Use Python's __eq__ by acquiring the GIL
                Python::with_gil(|py| {
                    // Bind the Py<PyAny> to this thread-local context
                    let a_bound = a.bind(py);
                    let b_bound = b.bind(py);
                    a_bound.eq(&b_bound).unwrap_or(false)
                })
            }
            // If types don't match, defer to Python's eq function
            (a, b) => Python::with_gil(|py| {
                let to_py = |item: &EditDistanceItem| -> Option<Py<PyAny>> {
                    match item {
                        EditDistanceItem::String(s) => s.into_py_any(py).ok(),
                        EditDistanceItem::Int(i) => i.into_py_any(py).ok(),
                        EditDistanceItem::Float(f) => f.into_py_any(py).ok(),
                        EditDistanceItem::Bool(b) => b.into_py_any(py).ok(),
                        EditDistanceItem::Object(obj) => Some(obj.clone_ref(py)),
                    }
                };

                match (to_py(a), to_py(b)) {
                    // if both are fine, defer to Python, otherwise assume False
                    (Some(a), Some(b)) => a.bind(py).eq(b.bind(py)).unwrap_or(false),
                    _ => false,
                }
            }),
        }
    }
}

impl<'source> FromPyObject<'source> for EditDistanceItem {
    fn extract_bound(obj: &Bound<'source, PyAny>) -> PyResult<Self> {
        // Try to extract each supported type in order
        if let Ok(val) = obj.extract::<String>() {
            return Ok(EditDistanceItem::String(val));
        } else if let Ok(val) = obj.extract::<i64>() {
            return Ok(EditDistanceItem::Int(val));
        } else if let Ok(val) = obj.extract::<f64>() {
            return Ok(EditDistanceItem::Float(val));
        } else if let Ok(val) = obj.extract::<bool>() {
            return Ok(EditDistanceItem::Bool(val));
        } else {
            // For any other type, store the Python object for later comparison
            let py_obj = obj.clone().unbind();
            return Ok(EditDistanceItem::Object(py_obj));
        }
    }
}

#[pyfunction(name = "universal_error_rate_array")]
pub fn universal_error_rate_array_py(
    predictions: &Bound<PyList>,
    references: &Bound<PyList>,
) -> PyResult<Vec<f64>> {
    // Create vectors to store the converted data
    let pred_vecs: Vec<Vec<EditDistanceItem>> = convert_to_edit_distance_item_vec(predictions)?;
    let ref_vecs: Vec<Vec<EditDistanceItem>> = convert_to_edit_distance_item_vec(references)?;

    // Create the vectors of references to vectors that the edit_distance function expects
    let pred_vec_refs: Vec<&Vec<EditDistanceItem>> = pred_vecs.iter().collect();
    let ref_vec_refs: Vec<&Vec<EditDistanceItem>> = ref_vecs.iter().collect();

    // Call a modified edit_distance implementation that works with EditDistanceItem
    let result = core::uer::universal_error_rate_array(&pred_vec_refs, &ref_vec_refs);

    Ok(result)
}

#[pyfunction(name = "universal_edit_distance")]
pub fn universal_edit_distance_array_py(
    predictions: &Bound<PyList>,
    references: &Bound<PyList>,
) -> PyResult<Vec<usize>> {
    // Create vectors to store the converted data
    let pred_vecs: Vec<Vec<EditDistanceItem>> = convert_to_edit_distance_item_vec(predictions)?;
    let ref_vecs: Vec<Vec<EditDistanceItem>> = convert_to_edit_distance_item_vec(references)?;

    // Create the vectors of references to vectors that the edit_distance function expects
    let pred_vec_refs: Vec<&Vec<EditDistanceItem>> = pred_vecs.iter().collect();
    let ref_vec_refs: Vec<&Vec<EditDistanceItem>> = ref_vecs.iter().collect();

    // Call a modified edit_distance implementation that works with EditDistanceItem
    let result = core::uer::universal_edit_distance_array(&pred_vec_refs, &ref_vec_refs);

    Ok(result)
}

fn convert_to_edit_distance_item_vec(
    pylist: &Bound<PyList>,
) -> PyResult<Vec<Vec<EditDistanceItem>>> {
    // Create vectors to store the converted data
    let mut vecs: Vec<Vec<EditDistanceItem>> = Vec::with_capacity(pylist.len());

    // Extract the data from Python
    for i in 0..pylist.len() {
        let item = pylist.get_item(i)?;
        let list = item.downcast::<PyList>()?;

        let mut inner: Vec<EditDistanceItem> = Vec::with_capacity(list.len());

        // Extract items from the inner lists, converting to EditDistanceItem
        for j in 0..list.len() {
            inner.push(list.get_item(j)?.extract::<EditDistanceItem>()?);
        }

        vecs.push(inner);
    }

    // Create the vectors of references to vectors that the edit_distance function expects
    return Ok(vecs);
}
