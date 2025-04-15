<p align="center">
  <a href="https://github.com/AlexDemure/gadutils">
    <a href="https://ibb.co/LhnNPPYp"><img src="https://i.ibb.co/JF53ddmk/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  A utility library for building clean and reusable data manipulation functions.
</p>

---
Utility Python library that centralizes all your data manipulation logic into one clean and structured place.
Instead of scattering helper functions across the codebase, it organizes them by data type — such as strings, decimals, dates, and more — making your application easier to maintain, test, and extend.

- Centralized and consistent data utilities
- Cleaner imports — no more `from datetime import datetime` vs `import datetime as dt`
- Reduces boilerplate and external dependencies
- Makes utility logic reusable, testable, and predictable

## Installation

```
pip install gadutils
```


## Usage

```python
from gadutils import strings, dates, decimals, fields, json, lists, paths, urls

print(strings.kebab("Hello World"))  # hello-world

date = dates.now()
print(dates.formatiso(date))   # "2025-04-10T12:34:56.789012+0000"

print(paths.current())         # "/home/user/project"
print(paths.define())          # "/home/user/project"
print(paths.define("/tmp"))    # "/tmp"

print(decimals.add(10.25, 5.75))        # Decimal('16.00')
print(decimals.split(100.05, 3))        # [Decimal('33.35'), Decimal('33.35'), Decimal('33.35')]

print(lists.unique([1, 2, 2, 3, 1]))         # [1, 2, 3]
print(lists.flatten([[1, 2], [3, [4]]]))     # [1, 2, 3, 4]
```
