All notable changes will be documented here.

---

## `1.0.3`
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