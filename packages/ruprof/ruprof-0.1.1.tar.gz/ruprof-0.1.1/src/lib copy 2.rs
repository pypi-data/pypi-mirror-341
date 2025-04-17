use pyo3::prelude::*;
use pyo3::types::{PyDict, PyAny, PyCFunction, PyTuple};
use std::time::Instant;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::ffi::CString;
use pyo3::ffi::{PyCode_Addr2Line, PyTrace_LINE, PyEval_SetTrace};
use pyo3::ffi::{PyFrameObject, PyObject };
mod hash;
use hash::hash_bytecode;


// Thread-safe struct to hold profiling data
#[pyclass]
struct Profiler {
    call_counts: Arc<Mutex<HashMap<String, u64>>>,
    total_times: Arc<Mutex<HashMap<String, f64>>>,
}

// unsafe extern "C" fn python_trace_callback(
//     obj: *mut PyObject,
//     frame: *mut PyFrameObject,
//     what: i32,
//     arg: *mut PyObject,
// ) -> i32 {
//     let profiler = &*(obj as *const Profiler);
//     profiler.trace_callback_rust(frame, what, arg)
// }

// c_code_number: Arc<Mutex<HashMap<u64, f64>>>,
#[pymethods]
impl Profiler {
    #[new]
    fn __new__() -> Self {
        Profiler {
            call_counts: Arc::new(Mutex::new(HashMap::new())),
            total_times: Arc::new(Mutex::new(HashMap::new())),
        }
    }

    fn enable(&self) {
        // Set the trace callback
        // PyEval_SetTrace(Box::new(self.trace_callback).into());
        // PyEval_SetTrace(python_trace_callback, self);
        // PyEval_SetTrace(Some(python_trace_callback), self as *const Profiler as *mut PyObject);
        println!("321123")
    }

    // fn trace_callback_rust(
    //     &self,
    //     frame: *mut PyFrameObject,
    //     what: i32,
    //     _arg: *mut PyObject,
    // ) -> i32 {
    //     println!("321123132");
    //     // unsafe {
    //     //     let code = (*frame).f_code;
    //     //     let name_ptr = pyo3::ffi::PyUnicode_AsUTF8((*code).co_name);
    //     //     let func_name = std::ffi::CStr::from_ptr(name_ptr)
    //     //         .to_string_lossy()
    //     //         .into_owned();

    //     //     match what {
    //     //         pyo3::ffi::PyTrace_CALL => {
    //     //             let mut start_times = self.start_times.lock().unwrap();
    //     //             start_times.insert(func_name.clone(), Instant::now());
    //     //         }
    //     //         pyo3::ffi::PyTrace_RETURN => {
    //     //             let mut start_times = self.start_times.lock().unwrap();
    //     //             if let Some(start) = start_times.remove(&func_name) {
    //     //                 let duration = start.elapsed().as_secs_f64();

    //     //                 let mut total_times = self.total_times.lock().unwrap();
    //     //                 *total_times.entry(func_name.clone()).or_insert(0.0) += duration;

    //     //                 let mut call_counts = self.call_counts.lock().unwrap();
    //     //                 *call_counts.entry(func_name).or_insert(0) += 1;
    //     //             }
    //     //         }
    //     //         _ => {}
    //     //     }
    //     // }
    //     0
    // }



    // The decorator function
    fn __call__(&self, py: Python<'_>, func: Py<PyAny>) -> PyResult<PyObject> {
        self.enable();
        // func.getattr(py, "__code__")?.extract::<PyCodeObject>(py)?;
        // func.getattr(py, "__code__") -> Py<PyAny>
        // .extract -> PyAny to Rust type (String / Struct)
        // ::<type> -> Rust Type explicitly

        // ======================== Register 
        let func_name = func.getattr(py, "__name__")?.extract::<String>(py)?;
        let code = func.getattr(py, "__code__")?; //PyCodeObject
        let co_code = code.getattr(py, "co_code")?; //*mut PyObject
        let bytecode_vec: Vec<u8> = co_code.extract(py)?;
        
        // For debugging - convert to hex string representation
        // let bytecode_hex = bytecode_vec.iter()
        //     .map(|b| format!("\\x{:02x}", b))
        //     .collect::<String>();
        // println!("Bytecode: b'{}'", bytecode_hex);

        // let bytecode_hash = hash_bytecode(&bytecode_vec, 0);
        // println!("Bytecode Hash: {}", bytecode_hash);
        // write a for loop ,iter the offset,byte from co_code,
        //  offset from 0 to length of co_code - 1
        for offset in 0..bytecode_vec.len() {
            let byte = bytecode_vec[offset];
            // Compute the hash for each byte
            let line_no = unsafe {
                PyCode_Addr2Line(code.as_ptr() as *mut pyo3::ffi::PyCodeObject, offset as i32)
            };
            println!("Byte: {:#04x}, Line: {}",  byte, line_no);
            // let byte_hash = hash_bytecode(&[byte], line_no as u64); // Assuming offset is 1 for simplicity
            // println!("Byte Hash at offset {} is {}", offset, byte_hash);
        }
    
        // ======================== profile by func
        // Create static C string for the function name
        let c_func_name = CString::new(func_name.clone())?;
        let c_func_name_static = Box::leak(c_func_name.into_boxed_c_str());
        
        // Clone the Arc<Mutex> containers to move into the closure
        let call_counts = self.call_counts.clone();
        let total_times = self.total_times.clone();
        let func_name_clone = func_name.clone();
        
        // Define the wrapper closure using thread-safe containers
        let wrapper = move |args: &Bound<'_, PyTuple>, kwargs: Option<&Bound<'_, PyDict>>| -> PyResult<Py<PyAny>> {
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
    fn get_stats(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
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

        Ok(stats.into_py(py))
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