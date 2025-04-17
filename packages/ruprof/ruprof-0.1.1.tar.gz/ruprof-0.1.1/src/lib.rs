use pyo3::prelude::*;
use pyo3::types::{PyDict, PyAny, PyCFunction, PyTuple};
use std::time::Instant;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::ffi::CString;
use pyo3::ffi::{PyFrameObject, PyObject as FFIPyObject};
use pyo3::ffi::{PyEval_SetTrace, PyTrace_LINE};
// use pyo3::ffi::{PyTrace_LINE, PyTrace_CALL, PyTrace_RETURN};
// use pyo3::ffi::{PyUnicode_AsUTF8AndSize};
// use std::ffi::CStr;

thread_local! {
    static FILEMAP: std::cell::RefCell<HashMap<u64, String>> = std::cell::RefCell::new(HashMap::new());
    static LASTTIME: std::cell::RefCell<Instant> = std::cell::RefCell::new(Instant::now());
}

#[pyclass]
struct Profiler {
    LastTime:  Arc<Instant>,
    line_time:  Arc<Mutex<HashMap<String, f64>>>,
    line_count: Arc<Mutex<HashMap<String, u32>>>,
    func_time:  Arc<Mutex<HashMap<String, f64>>>,
    func_count: Arc<Mutex<HashMap<String, u32>>>,
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
            LastTime:  Arc::new(Instant::now()),
            line_time:  Arc::new(Mutex::new(HashMap::new())),
            line_count: Arc::new(Mutex::new(HashMap::new())),
            func_time:  Arc::new(Mutex::new(HashMap::new())),
            func_count: Arc::new(Mutex::new(HashMap::new())),
        }
    }
    fn get_stats(&self, py: Python<'_>) -> PyResult<PyObject> {
        let stats = PyDict::new(py);
        // println!("{:?}",self.func_count.lock().unwrap());
        // println!("{:?}",self.func_time.lock().unwrap());
        // FILEMAP.with(|map| {println!("{:?}", map.borrow());});


        // // Func Count and Time
        // if let (Ok(counts), Ok(times)) = (self.func_count.lock(), self.func_time.lock()) {
        //     for (name, count) in counts.iter() {
        //         let total_time = times.get(name).unwrap_or(&0.0);
        //         let stat_dict = PyDict::new(py);
        //         stat_dict.set_item("count", *count)?;
        //         stat_dict.set_item("time", *total_time)?;
        //         stats.set_item(name, stat_dict)?;
        //     }
        // }

        // Func Line Count and Time
        if let (Ok(counts), Ok(times)) = (self.line_count.lock(), self.line_time.lock()) {
            for (name, count) in counts.iter() {
                let total_time = times.get(name).unwrap_or(&0.0);
                let stat_dict = PyDict::new(py);
                stat_dict.set_item("count", *count)?;
                stat_dict.set_item("time", *total_time)?;
                stats.set_item(name, stat_dict)?;
            }
        }
        


        
        Ok(stats.into())
    }
    // The decorator function
    unsafe fn __call__(&self, py: Python<'_>, func: Py<PyAny>) -> PyResult<PyObject> {
        self.enable();

        // 
        let func_name = func.getattr(py, "__name__")?.extract::<String>(py)?;
        let __code__ = func.getattr(py, "__code__")?;
        // let filename = __code__.getattr(py, "co_filename")?.extract::<String>(py)?;
        let line_no = __code__.getattr(py, "co_firstlineno")?.extract::<i32>(py)?;
        let co_filename = __code__.getattr(py, "co_filename")?.as_ptr();
        
        // println!("__call__ Function name: {:?}, {:?}", func_name, filename);
        // println!("__call__ Line number: {:?}", line_no);
        // println!("__call__ co_filename: {:?}", co_filename);
        
        
        // Create static C string for the function name
        let c_func_name = CString::new(func_name.clone())?;
        let c_func_name_static = Box::leak(c_func_name.into_boxed_c_str());
        
        // Clone the Arc<Mutex> containers to move into the closure
        let func_count = self.func_count.clone();
        let func_time = self.func_time.clone();
        
        let key = format!("{:?}:{:?}", co_filename, line_no);
        // closure FnOnce for wrapping
        let wrapper = move |args: &Bound<'_, PyTuple>, kwargs: Option<&Bound<'_, PyDict>>| -> PyResult<PyObject> {
            let py = args.py();
            let start = Instant::now();
            let result = func.call(py, args, kwargs)?;            // Call the original function
            let duration = start.elapsed().as_secs_f64();

            // func_count
            {if let Ok(mut counts) = func_count.lock() {
                let count = counts.entry(key.clone()).or_insert(0);
                *count += 1;
            }}
            // func_time
            {if let Ok(mut times) = func_time.lock() {
                let total_time = times.entry(key.clone()).or_insert(0.0);
                *total_time += duration;
            }}
            Ok(result)
        };
    
        // Create the Python callable with the correct closure
        let py_func = PyCFunction::new_closure(py, Some(c_func_name_static), None, wrapper)?;
        Ok(py_func.into())
    }
}



impl Profiler {
    fn trace_callback_rust(
        &self,
        frame: *mut PyFrameObject,
        what: i32,
        _arg: *mut FFIPyObject,
    ) -> i32 {
        // println!("{:?}", what==PyTrace_CALL);
        if what == PyTrace_LINE {
            unsafe {
                let code = (*frame).f_code;
                let line_no = (*frame).f_lineno as u64;

                // k:v - filename ptr <u64> : filename<String>
                let co_filename = (*code).co_filename;
                let key = format!("{:?}:{}", co_filename, line_no);
                // let utf8_ptr = PyUnicode_AsUTF8AndSize(co_filename, std::ptr::null_mut());
                // let filename = CStr::from_ptr(utf8_ptr)
                //     .to_str()
                //     .unwrap_or("<invalid>")
                //     .to_string();  // Convert to owned String
                
                let line_count = self.line_count.clone();
                let line_time = self.line_time.clone();
                // line_count
                {
                    match line_count.lock() {
                        Ok(mut counts) => {
                            let count = counts.entry(key.clone()).or_insert(0);
                            *count += 1;
                            // println!("line_count = {:?}", count);
                        }
                        Err(e) => println!("line_count lock failed: {:?}", e),
                    }
                };

                // line_time
                LASTTIME.with(|last_time| {
                    let mut last_time = last_time.borrow_mut(); // Mutable borrow
                    
                    if let Ok(mut times) = line_time.lock() {
                        // println!("line_time = {:?}", last_time.elapsed().as_secs_f64());
                        let duration = last_time.elapsed().as_secs_f64();
                        let total_time = times.entry(key.clone()).or_insert(0.0);
                        *total_time += duration;
                        *last_time = Instant::now(); // Reset the instant
                    } else {
                        println!("line_time lock failed: {:?}", line_time.lock().err());
                    }
                });
        
                // let id = filename+
                // FILEMAP.with(|map| {
                //     let mut map = map.borrow_mut();
                //     map.insert(id, format!(
                //         "{} in {} at line {}",
                //         func_name.to_string_lossy(),
                //         filename.to_string_lossy(),
                //         line_no
                //     ));
                //     println!("trace_callback_rust - CALL: {} in {}:{}", 
                //         func_name.to_string_lossy(),
                //         filename.to_string_lossy(),
                //         line_no
                //     );
                //     println!("Current filemap: {:?}", *map);
                // });


                // let code = (*frame).f_code;
                // let filename = CStr::from_ptr((*code).co_filename as *const i8);
                // let func_name = CStr::from_ptr((*code).co_name as *const i8);
                // let line_no = (*frame).f_lineno;
                // println!("{:?}:{:?}", filename, func_name);
                // let id = Instant::now().elapsed().as_nanos() as u64;
                // FILEMAP.with(|map| {
                //     let mut map = map.borrow_mut();
                //     map.insert(id, format!(
                //         "{} in {} at line {}",
                //         func_name.to_string_lossy(),
                //         filename.to_string_lossy(),
                //         line_no
                //     ));
                //     println!("trace_callback_rust - CALL: {} in {}:{}", 
                //         func_name.to_string_lossy(),
                //         filename.to_string_lossy(),
                //         line_no
                //     );
                //     println!("Current filemap: {:?}", *map);
                // });
            }
        }
        0
    }
    unsafe fn enable(&self) {
        PyEval_SetTrace(Some(python_trace_callback), 
                        self as *const Profiler as *mut FFIPyObject);
    }
}

use pyo3::prelude::*;
use rayon::prelude::*;
use regex::Regex;
use std::fs;
use std::path::Path;

#[allow(unsafe_op_in_unsafe_fn)]
#[pyfunction]
fn add_decorator(file_paths: Vec<String>, decorator: String) -> PyResult<HashMap<String, String>> {
    // Create a thread pool for parallel processing
    let pool = rayon::ThreadPoolBuilder::new()
        .build()
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Thread pool error: {}", e)))?;

    // Process files in parallel
    let results: Vec<(String, String)> = pool.install(|| {
        file_paths
            .par_iter()
            .filter_map(|path| {
                // Convert to absolute path
                let abs_path = match fs::canonicalize(Path::new(path)) {
                    Ok(p) => p.to_string_lossy().into_owned(),
                    Err(_) => return None,
                };

                // Read file content
                let content = match fs::read_to_string(path) {
                    Ok(c) => c,
                    Err(_) => return None,
                };

                // Process the content to add decorators
                let decorated_content = add_decorator_to_functions(&content, &decorator);
                Some((abs_path, decorated_content))
            })
            .collect()
    });

    // Convert results to HashMap
    let result_map: HashMap<String, String> = results.into_iter().collect();

    Ok(result_map)
}

fn add_decorator_to_functions(content: &str, decorator: &str) -> String {
    // Regex to match 'def' statements, capturing the whole line
    let re = Regex::new(r"(?m)^(def\s+[^\n#]*)$").unwrap();
    let mut result = content.to_string();
    let mut offset = 0;

    // Find all matches and insert decorator
    for mat in re.find_iter(content) {
        let start = mat.start() + offset;
        let indent = content[..mat.start()]
            .chars()
            .rev()
            .take_while(|&c| c == ' ')
            .count();
        let decorator_line = format!("{}@{}\n", " ".repeat(indent), decorator);
        
        result.insert_str(start, &decorator_line);
        offset += decorator_line.len();
    }

    result
}


#[pymodule]
fn ruprof(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Profiler>()?;
    m.add_function(wrap_pyfunction!(add_decorator, m)?)?;
    Ok(())
}