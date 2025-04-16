## Bunch

A simple Python class that allows dictionary-style and attribute-style access to data interchangeably. Think of it as a lightweight object wrapper for dictionaries — great for config objects, JSON responses, or anything else you'd normally throw in a dict.

### <ins> Features </ins>

- Access keys as attributes or like a dictionary
- Convert from regular dictionaries
- Pretty-printed JSON representation
- Check if a value exists
- Fully compatible with `in`, `.keys()`, `.items()`, etc.

### <ins> Installation </ins>

You can install this package via PIP: _pip install bunch_

### <ins> Usage </ins>

```python
from bunch import Bunch

my_bunch = Bunch({'name': 'Jane', 'age': 30})

print(my_bunch.name)  # Output: Jane
print(my_bunch['age'])  # Output: 30
```
