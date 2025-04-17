use pyo3::prelude::*;
use pyo3::types::{PyDict, PyAny, PyCFunction, PyTuple};
use std::time::Instant;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::ffi::CString;

// Thread-safe struct to hold profiling data
#[pyclass]
struct Profiler {
    call_counts: Arc<Mutex<HashMap<String, u64>>>,
    total_times: Arc<Mutex<HashMap<String, f64>>>,
}

#[pymethods]
impl Profiler {
    #[new]
    fn __new__() -> Self {
        Profiler {
            call_counts: Arc::new(Mutex::new(HashMap::new())),
            total_times: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    // The decorator function
    fn __call__(&self, py: Python<'_>, func: Py<PyAny>) -> PyResult<PyObject> {
        let func_name = func.getattr(py, "__name__")?.extract::<String>(py)?;
        // println!("Decorating function: {}", func_name);
    
        // Create static C string for the function name
        let c_func_name = CString::new(func_name.clone())?;
        let c_func_name_static = Box::leak(c_func_name.into_boxed_c_str());
        
        // Clone the Arc<Mutex> containers to move into the closure
        let call_counts = self.call_counts.clone();
        let total_times = self.total_times.clone();
        let func_name_clone = func_name.clone();
        
        // Define the wrapper closure using thread-safe containers
        let wrapper = move |args: &Bound<'_, PyTuple>, kwargs: Option<&Bound<'_, PyDict>>| -> PyResult<PyObject> {
            let py = args.py();
            // println!("Wrapper called for: {}", func_name_clone);
            let start = Instant::now();
    
            // Call the original function
            let result = func.call(py, args, kwargs)?;
            let duration = start.elapsed().as_secs_f64();
            
            // Update the count for this function using thread-safe mutex
            {
                if let Ok(mut counts) = call_counts.lock() {
                    let count = counts.entry(func_name_clone.clone()).or_insert(0);
                    *count += 1;
                    // println!("Updated count for {}: {}", func_name_clone, *count);
                }
            }
            
            // Update the total time for this function
            {
                if let Ok(mut times) = total_times.lock() {
                    let total_time = times.entry(func_name_clone.clone()).or_insert(0.0);
                    *total_time += duration;
                }
            }
    
            Ok(result)
        };
    
        // Create the Python callable with the correct closure
        let py_func = PyCFunction::new_closure(py, Some(c_func_name_static), None, wrapper)?;
        Ok(py_func.into())
    }

    // Method to get recorded stats
    fn get_stats(&self, py: Python<'_>) -> PyResult<PyObject> {
        let stats = PyDict::new(py);
        
        // Use thread-safe locking to access the HashMaps
        if let (Ok(counts), Ok(times)) = (self.call_counts.lock(), self.total_times.lock()) {
            // println!("Stats - Number of functions: {}", counts.len());

            for (name, count) in counts.iter() {
                let total_time = times.get(name).unwrap_or(&0.0);
                let stat_dict = PyDict::new(py);
                stat_dict.set_item("calls", *count)?;
                stat_dict.set_item("total_time", *total_time)?;
                stats.set_item(name, stat_dict)?;
            }
        }

        Ok(stats.into())
    }

    // fn print_stats(&self, py: Python<'_>) {
    //     println!("{?},", self.get_stats(py));
    // }
}

#[pymodule]
fn ruprof(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Profiler>()?;
    Ok(())
}