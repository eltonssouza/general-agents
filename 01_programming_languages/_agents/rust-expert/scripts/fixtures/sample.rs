use std::rc::Rc;
use std::cell::RefCell;

static mut COUNTER: u32 = 0;

extern "C" {
    fn abs(x: i32) -> i32;
}

#[no_mangle]
pub extern "C" fn exported() {}

fn first(names: &Vec<String>, label: &String) -> usize {
    let n = names.len() as u8;
    for i in 0..names.len() {
        let _ = names[i].clone();
    }
    let v: Option<u32> = None;
    v.unwrap();
    n as usize
}

fn read(p: *const u8) -> u8 {
    unsafe { *p }
}

fn read_ok(p: *const u8) -> u8 {
    // SAFETY: the caller guarantees that p is valid and aligned.
    unsafe { *p }
}

/// # Safety
/// p must be valid.
unsafe fn raw(p: *const u8) -> u8 { *p }

fn shared() {
    let _s = Rc::new(RefCell::new(1));
    let h = std::thread::spawn(|| { println!("x"); });
    h.join().unwrap();
}

fn cast(x: &u32) -> *const u32 { x as *const u32 }

unsafe fn bare_deref(p: *const u8) -> u8 {
    *p
}

unsafe fn explicit(p: *const u8) -> u8 {
    // SAFETY: p is valid by contract.
    unsafe { *p }
}

#[cfg(test)]
mod tests {
    #[test]
    fn t() { Some(1).unwrap(); }
}
