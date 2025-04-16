use polars::prelude::*;

use pyo3_polars::derive::polars_expr;

use ahash::RandomState;

#[polars_expr(output_type=UInt64)]
fn oldhash(inputs: &[Series]) -> PolarsResult<Series> {
    let s = inputs.get(0).expect("no series received");

    let rs = RandomState::with_seeds(0, 0, 0, 0);
    let mut h: Vec<u64> = vec![];
    let ser_name: &str = s.name();

    match s.vec_hash(rs, &mut h) {
        Ok(_) => Ok(UInt64Chunked::from_vec(&ser_name, h).into_series()),
        Err(res) => Err(res),
    }
}
