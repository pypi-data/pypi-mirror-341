# Polars legacy hash

For a specific project, I needed to preserve the hashing behaviour of polars 0.20.10 (or the underlying ahash 0.8.7),
whilst also wanting to upgrade polars itself. 

For now this plugin specifically caters to 0.20.10, but in principle could be generalised. See also [Polars Hash](https://github.com/ion-elgreco/polars-hash) which is a more general solution to this, which is coupled to a specific point in time in the history of polars. If there ever comes a use case for this, I expect to move to some version of versioning akin to stub libraries e.g. 0.20.10.20250415 and deploy these from seperate branches to avoid having to bundle multiple polars binaries into the same wheel.

## Usage
```python
import polars as pl
import polars_legacy_hash as plh
df = pl.DataFrame({"a": [-42, 13], "b": [-42, 0]})
result = pl.select(plh.oldhash(df.to_struct("test")))

```
For correctness checking, the CI runs `test_expectations.py` under polars 0.20.10 to
confirm that the test values in the fixtures (defined in tests/conftest.py) are consistent with polars itself.


## Development
The plugin is built with maturin, and uv is setup to rebuild an editable install whenever the rust part of the plugin changes. This means the simplest way to run the tests is
`uv run pytest -rP`
