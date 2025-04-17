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
use pyo3::ffi::{PyUnicode_AsUTF8AndSize};
use std::ffi::CStr;


#[pyclass]
struct Profiler {
    filemap : Arc<Mutex<HashMap<u64, String>>>,
}

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

#[pymethods]
impl Profiler {
    #[new]
    fn __new__() -> Self {
        Profiler {
            filemap : Arc::new(Mutex::new(HashMap::new())),
        }
    }

    // The decorator function
    unsafe fn __call__(&self, py: Python<'_>, func: Py<PyAny>) -> PyResult<PyObject> {
        self.enable();
        let func_name = func.getattr(py, "__name__")?.extract::<String>(py)?;
    
        // Create static C string for the function name
        let c_func_name = CString::new(func_name.clone())?;
        let c_func_name_static = Box::leak(c_func_name.into_boxed_c_str());
        
        let wrapper = move |args: &Bound<'_, PyTuple>, kwargs: Option<&Bound<'_, PyDict>>| -> PyResult<PyObject> {
            let py = args.py();
            let result = func.call(py, args, kwargs)?;            // Call the original function
            Ok(result)
        };
    
        // Create the Python callable with the correct closure
        let py_func = PyCFunction::new_closure(py, Some(c_func_name_static), None, wrapper)?;
        Ok(py_func.into())
    }

}

thread_local! {
    static FILEMAP: std::cell::RefCell<HashMap<u64, String>> = std::cell::RefCell::new(HashMap::new());
}

impl Profiler {
    fn trace_callback_rust(
        &self,
        frame: *mut PyFrameObject,
        what: i32,
        _arg: *mut FFIPyObject,
    ) -> i32 {
        // println!("{:?}", what==PyTrace_CALL);
        if what == PyTrace_CALL {
            unsafe {
                let code = (*frame).f_code;
                let filename = CStr::from_ptr((*code).co_filename as *const i8);
                let func_name = CStr::from_ptr((*code).co_name as *const i8);
                let line_no = (*frame).f_lineno;
                
                let id = Instant::now().elapsed().as_nanos() as u64;
                FILEMAP.with(|map| {
                    let mut map = map.borrow_mut();
                    map.insert(id, format!(
                        "{} in {} at line {}",
                        func_name.to_string_lossy(),
                        filename.to_string_lossy(),
                        line_no
                    ));
                    println!("trace_callback_rust - CALL: {} in {}:{}", 
                        func_name.to_string_lossy(),
                        filename.to_string_lossy(),
                        line_no
                    );
                    println!("Current filemap: {:?}", *map);
                });
            }
        }


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