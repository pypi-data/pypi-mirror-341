# California Virtual Campus API
A simple API for the California Virtual Campus platform.
---

Documentation can be found at:
https://cvc-api.github.io/

Installation:
```bash
python -m pip install CaliforniaVirtualCampusAPI 
```

Update:
```bash
python -m pip install CaliforniaVirtualCampusAPI --upgrade
```

To use the package in your program, please import the package:
```python
from cvc import *
```

Uninstallation:
```bash
python -m pip uninstall CaliforniaVirtualCampusAPI 
```

## Usage
Request a particular list of courses and retrieve all of their data.

Example:
```python
from cvc import *

courseIDs = getCourseIDsBySearch("Pasadena City College", "COMP122", "CS2", "FUNDAMENTALS OF COMPUTER SCIENCE I")
getCourseContentByID(courseIDs[0]).printAll()
```

## License
This project is also licensed under the [Apache 2.0 License](http://www.apache.org/licenses/LICENSE-2.0). See LICENSE for more details.

The course data used by this project is provided by California Virtual Campus and is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).