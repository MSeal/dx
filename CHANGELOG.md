All notable changes will be documented here.

---
## `1.1.3`
_2022-08-05_
### Added
- Helper text for adjusting settings after a dataset has been truncated
- `.reset_index()` when a custom/MultiIndex is used to preserve `0-n` row numbers at the `index` level
- Support for geopandas GeoDataFrames and GeoSeries objects
- More tests!

### Changed
- `default` display mode (vanilla pandas) renamed to `plain`

### Fixed
- Properly pass `metadata` through during the `IPython.display` calls to render dataresource/dx formatted data

<img width="568" alt="image" src="https://user-images.githubusercontent.com/7707189/182971951-52b440ae-f894-4eb0-8941-3cadd78aef0a.png">


## `1.1.1`-`1.1.2`
_2022-07-22_
### Added
- Additional metadata sent to frontends to triage issues with output sizes and `dx` settings
### Fixed
- `simple`/`enhanced` display modes no longer raise JSON errors trying to serialize `pd.NA` values
- `SAMPLE_METHOD` returning incorrect value (`True` instead of `DXSampleMethod`) when compared with `COLUMN_SAMPLE_METHOD` and `ROW_SAMPLE_METHOD`
- Truncating rows no longer alters dtypes by adding `...` values
  
## `1.1.0`
_2022-07-22_
### **Added**
- Direct support for `application/vnd.dataresource+json` media type display formatting
- reverting all settings to `pandas` defaults with `dx.reset()` or switching to the `DISPAY_MODE` setting to `default`
- `pydantic` dependency for BaseSettings use
    - `pandas`-inspired `dx.set_option(setting_name, setting_value)` 
    - `dx.set_display_mode()` convenience function for globally switching between `simple` (simpleTable/DEX), `enhanced` (GRID), and `default` (vanilla pandas)
- Auto-truncating rows and columns of `pd.DataFrame` objects based on `DISPLAY_MAX_ROWS`, `DISPLAY_MAX_COLUMNS`, and `MAX_RENDER_SIZE_BYTES` (1MB default) size limits before rendering (for `simple` & `enhanced` display modes), with blueprintjs flavored warnings
    - `SAMPLING_MODE` setting to better control how truncating happens ("first", "last", "outer", "inner", and "random" options)
    - `RANDOM_SEED` setting for random sampling

### **Fixed**
- Support for non-string column and index values (possibly temporary) to allow `build_table_schema` to work with `pd.MultiIndex` values

## `1.0.4`
_2022-05-06_
### **Fixed**
* Lowered the minimum required `ipython` version from `8.2.0` to `7.31.1`
  
## `1.0.3`
_2022-04-26_
### **Fixed**
* `dx.register()` (`dx.enable()`, deprecated) and `dx.deregister()` (`dx.disable()`, deprecated) will now update the default display formatting for pandas `DataFrame` objects as intended

## `1.0.2`
_2022-04-25_
### **Fixed**
* Updated minimum `python` version to `3.8` (down from `3.9.6` in 1.0.0)

### **Added**
* Custom `IPython` formatter for [Noteable](https://app.noteable.io/) environments
* Additional data type support for `display()` / `dx()`: 
    * any tabular structure (lists of dicts, dict of `{column: [values]}`, etc) that can be loaded into a pandas `DataFrame`
    * `.csv` and `.json` file paths