
# Timsort Implementation in Python

## Overview

This project provides a simplified implementation of the **Timsort sorting algorithm**, focusing on the segmentation of lists into ordered subsequences (increasing, decreasing, or unsorted). This script is intended as a teaching aid for understanding the basics of Timsort, a hybrid sorting algorithm combining merge sort and insertion sort principles.

## Features

- **Segment Representation**: Splits lists into segments marked as increasing, decreasing, or unsorted.
- **Customizable Sorting**: Supports custom key functions for sorting elements.
- **Classes**:
  - `Segment`: Represents a segment of the list.
  - `IncDecRuns`: Splits the list into segments based on order type.

## File Information

- **File Name**: `timsort.py`
- **Author**: John Longley
- **Date**: October 2022
- **Course**: Inf2-IADS (2022-23) Coursework 1, Part A

## Code Structure

### Segment Class

Represents a list segment with properties:
- `start`: Starting index of the segment.
- `end`: Ending index (exclusive).
- `tag`: The type of segment (`Inc`, `Dec`, or `Unsorted`).

Methods:
- `len()`: Returns the length of the segment.
- `__repr__()`: String representation for debugging purposes.

### IncDecRuns Class

Responsible for:
- Splitting the list into `Inc` (increasing) and `Dec` (decreasing) segments.
- Maintaining boundary indices and segment types.

Initialization Parameters:
- `L`: List to be segmented.
- `key`: Custom key function to compare elements.

## Requirements

- Python 3.6 or later.

## Usage

1. Import the script into your project:
   ```python
   from timsort import IncDecRuns
   ```
2. Create an instance of `IncDecRuns` to split a list into ordered segments:
   ```python
   runs = IncDecRuns(my_list)
   ```
3. Access and manipulate segments for further sorting or analysis.

## Examples

### Splitting a List

```python
from timsort import IncDecRuns

L = [3, 5, 2, 8, 6, 4]
runs = IncDecRuns(L)
print(runs)  # Output will show segmented representation
```

### Custom Key Function

```python
from timsort import IncDecRuns

L = ['apple', 'banana', 'cherry']
runs = IncDecRuns(L, key=len)
print(runs)  # Segments based on string length
```

## Future Improvements

- **Merge Segments**: Implement logic to merge segments for a complete Timsort.
- **Performance Optimization**: Enhance segment splitting for large datasets.
- **Additional Features**: Support advanced use cases like stability checks and adaptive runs.

## License

This project is intended for educational purposes and follows academic integrity guidelines. For commercial use, please contact the author.
