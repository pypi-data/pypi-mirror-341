use pyo3::prelude::*;

mod bindings;
mod core;

use bindings::*;

/// A Python module implemented in Rust.
#[pymodule]
fn universal_edit_distance(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Character error rate
    m.add_function(wrap_pyfunction!(cer::character_edit_distance_array_py, m)?)?;
    m.add_function(wrap_pyfunction!(cer::character_error_rate_py, m)?)?;
    m.add_function(wrap_pyfunction!(cer::character_error_rate_array_py, m)?)?;

    // Universal error rate
    m.add_function(wrap_pyfunction!(uer::universal_edit_distance_array_py, m)?)?;
    m.add_function(wrap_pyfunction!(uer::universal_error_rate_array_py, m)?)?;

    // Word error rate
    m.add_function(wrap_pyfunction!(wer::word_edit_distance_array_py, m)?)?;
    m.add_function(wrap_pyfunction!(wer::word_error_rate_py, m)?)?;
    m.add_function(wrap_pyfunction!(wer::word_error_rate_array_py, m)?)?;
    Ok(())
}
