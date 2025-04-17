# Pyreadable
A lightweight Python module to check weather a PDF file contains only machine readable text or not.

``` python
from pyreadable import is_machine_readable

# you can also provide margin_pts, dpi for the pdf. By default these parameters are set to 72.
print(is_machine_readable(file_path))
```
Sample Output:
``` bash
>>> (True,1.0)
```