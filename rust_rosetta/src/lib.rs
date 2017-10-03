#![crate_type = "dylib"]

#[no_mangle]
pub extern "C" fn cholesky(mat: &[f64], res: &mut [f64], n: usize) {
    for i in 0..n {
        for j in 0..(i+1){
            let mut s = 0.0;
            for k in 0..j {
                s += res[i * n + k] * res[j * n + k];
            }
            res[i * n + j] = if i == j { (mat[i * n + i] - s).sqrt() } else { (1.0 / res[j * n + j] * (mat[i * n + j] - s)) };
        }
    }
}
