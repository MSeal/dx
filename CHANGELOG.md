All notable changes will be documented here.

---

## [1.0.0]() - 2022-04-25
### **Added**
* Custom `IPython` formatter for [Noteable](https://app.noteable.io/) environments
* Additional data type support for `display()` / `dx()`: 
    * any tabular structure (lists of dicts, dict of `{column: [values]}`, etc) that can be loaded into a pandas `DataFrame`
    * `.csv` and `.json` file paths