use pyo3::prelude::*;
use pyo3::types::{PyDict, PyAny, PyCFunction, PyTuple};
use std::time::Instant;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::ffi::CString;
use pyo3::ffi::{PyFrameObject};
use pyo3::ffi::{PyEval_SetTrace};
use pyo3::ffi::PyObject as FFIPyObject;
use pyo3::ffi::{PyTrace_LINE, PyTrace_CALL, PyTrace_RETURN};
// use pyo3::ffi::{PyFrame_GetCode};


unsafe extern "C" fn python_trace_callback(
    obj: *mut FFIPyObject,
    frame: *mut PyFrameObject,
    what: i32,
    arg: *mut FFIPyObject,
) -> i32 {
    let profiler = &*(obj as *const Profiler);
    profiler.trace_callback_rust(frame, what, arg);
    0
}

// Thread-safe struct to hold profiling data
#[pyclass]
struct Profiler {
    call_counts: Arc<Mutex<HashMap<String, u64>>>,
    total_times: Arc<Mutex<HashMap<String, f64>>>,
    filename: Arc<Mutex<HashMap<u64, String>>>
}

#[pymethods]
impl Profiler {
    #[new]
    fn __new__() -> Self {
        Profiler {
            call_counts: Arc::new(Mutex::new(HashMap::new())),
            total_times: Arc::new(Mutex::new(HashMap::new())),
            filename: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    // Method to get recorded stats
    fn get_stats(&self, py: Python<'_>) -> PyResult<PyObject> {
        let stats = PyDict::new(py);
        
        // Use thread-safe locking to access the HashMaps
        if let (Ok(counts), Ok(times), Ok(filename_map)) = (self.call_counts.lock(), self.total_times.lock(), self.filename.lock()) {
            // println!("Stats - Number of functions: {}", counts.len());

            for (name, count) in counts.iter() {
                let total_time = times.get(name).unwrap_or(&0.0);
                let stat_dict = PyDict::new(py);
                stat_dict.set_item("calls", *count)?;
                stat_dict.set_item("total_time", *total_time)?;
                stat_dict.set_item("filename", &*filename_map)?;
                stats.set_item(name, stat_dict)?;
            }
        }

        Ok(stats.into())
    }

    // fn print_stats(&self, py: Python<'_>) {
    //     println!("{?},", self.get_stats(py));
    // }


    // The decorator function
    unsafe fn __call__(&self, py: Python<'_>, func: Py<PyAny>) -> PyResult<PyObject> {
        self.enable();
        let func_name = func.getattr(py, "__name__")?.extract::<String>(py)?;
        let filename = func.getattr(py, "__code__");
        // if filename not in self.filename_map , insert filename_map[&filename] = co_filename;
        // Insert into filename map if not present
        
        // println!("type of filename : {:?}", filename);
        // println!("filename : {:?}", filename);
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
}

use pyo3::ffi::{PyUnicode_AsUTF8AndSize};
use std::ffi::CStr;

impl Profiler {
    fn trace_callback_rust(
        &self,
        frame: *mut PyFrameObject,
        what: i32,
        _arg: *mut FFIPyObject,
    ) -> i32 {
        unsafe {
            let code = (*frame).f_code;
            let co_code = (*code).co_code;
            // use pyo3::ffi::{PyBytes_Check, PyBytes_Size,PyBytes_AsString};
            // use std::ffi::CStr;
            // if !co_code.is_null() && PyBytes_Check(co_code) != 0 {
            //     let size = PyBytes_Size(co_code); // Get length of bytes
            //     let data = PyBytes_AsString(co_code); // Get raw pointer to bytes
            //     if !data.is_null() && size >= 0 {
            //         // Convert to Rust string (assuming it's safe to interpret as UTF-8 for display)
            //         let bytes = std::slice::from_raw_parts(data as *const u8, size as usize);
            //         match CStr::from_ptr(data).to_str() {
            //             Ok(s) => println!("co_code: {:?}", s), // Print as string (may not be readable)
            //             Err(_) => println!("co_code: {:?} (non-UTF-8 bytes)", bytes),
            //         }
            //     } else {
            //         println!("co_code: invalid bytes object");
            //     }
            // } else {
            //     println!("co_code: not a bytes object or null");
            // }
            let line_no = pyo3::ffi::PyFrame_GetLineNumber(frame);
            let co_filename = (*code).co_filename; // PyObject
            let co_filename_key: u64 = (*code).co_filename as u64; // convert co_filename to u64 as key

            let mut filename_map = self.filename.lock().unwrap();
            if !filename_map.contains_key(&co_filename_key) {
                let mut size: isize = 0;
                let utf8_ptr = PyUnicode_AsUTF8AndSize(co_filename, &mut size);
                let filename = CStr::from_ptr(utf8_ptr)
                    .to_str()
                    .unwrap_or("<invalid>")
                    .to_string();  // Convert to owned String
                println!("{:?}, {:?}, {:?}", co_filename, co_filename_key, filename);
                filename_map.insert(co_filename_key, filename);
            }

            match what {
                PyTrace_CALL => { // 0 
                    let x = 1;
                    // println!("1");
                }
                // PyTrace_EXCEPTION => { // 1
                PyTrace_LINE => { // 2
                    let x = 2;
                    // println!("2");
                }
                PyTrace_RETURN => { // 3
                    let x = 3;
                    // println!("3");
                }
                _ => {}
            }
        }


        // unsafe {
        //     let code = (*frame).f_code;
        //     let name_ptr = pyo3::ffi::PyUnicode_AsUTF8((*code).co_name);
        //     let func_name = std::ffi::CStr::from_ptr(name_ptr)
        //         .to_string_lossy()
        //         .into_owned();

        //     match what {
        //         pyo3::ffi::PyTrace_CALL => {
        //             let mut start_times = self.start_times.lock().unwrap();
        //             start_times.insert(func_name.clone(), Instant::now());
        //         }
        //         pyo3::ffi::PyTrace_RETURN => {
        //             let mut start_times = self.start_times.lock().unwrap();
        //             if let Some(start) = start_times.remove(&func_name) {
        //                 let duration = start.elapsed().as_secs_f64();

        //                 let mut total_times = self.total_times.lock().unwrap();
        //                 *total_times.entry(func_name.clone()).or_insert(0.0) += duration;

        //                 let mut call_counts = self.call_counts.lock().unwrap();
        //                 *call_counts.entry(func_name).or_insert(0) += 1;
        //             }
        //         }
        //         _ => {}
        //     }
        // }
        0
    }

    unsafe fn enable(&self) {
        PyEval_SetTrace(Some(python_trace_callback), 
                        self as *const Profiler as *mut FFIPyObject);
    }

}

#[pymodule]
fn ruprof(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Profiler>()?;
    Ok(())
}