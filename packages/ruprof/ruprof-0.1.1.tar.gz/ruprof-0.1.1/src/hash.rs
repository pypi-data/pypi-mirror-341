pub fn hash_bytecode(bytes: &[u8], offset: i32) -> u64 {
    let mut hash: u64 = 23;
    for &byte in bytes {
        hash = hash.wrapping_add(byte as u64).wrapping_mul(offset as u64);
    }
    hash
}
