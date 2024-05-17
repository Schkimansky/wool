use std::ffi::CStr;

pub type PyStr = *const i8;

pub fn PyStr_to_str(c: *const i8) -> &'static str {
    // Converts a python string to a rust string: &'static str.
    let c_str = unsafe { CStr::from_ptr(c) };

    match c_str.to_str() {
        Ok(c_str) => return c_str,
        Err(_) => panic!("Invalid UTF-8 sequence of a parameter."),
    }
}