# ThanosPy 🫰

[![PyPI version](https://badge.fury.io/py/py-thanos-snap.svg)](https://badge.fury.io/py/py-thanos-snap) <!-- Update when published -->
[![CI Status](https://github.com/manyan-chan/thanosPy/actions/workflows/python-package.yml/badge.svg)](https://github.com/manyan-chan/thanosPy/actions/workflows/python-package.yml) <!-- Update USERNAME/REPO -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Versions](https://img.shields.io/pypi/pyversions/py-thanos-snap.svg) <!-- Update when published -->

*"Perfectly balanced... as all things should be."*

`thanosPy` provides a simple function, `snap()`, that takes a Python built-in data structure or type and randomly removes approximately half of its contents, returning the result as the same type.

## Features

*   **One Function:** Simple `snap(data)` interface.
*   **Type Preservation:** Output type matches input type (e.g., list in -> list out, tuple in -> tuple out).
*   **Random Removal:** Uses `random.sample` for unbiased removal where applicable.
*   **Supported Types:**
    *   `list`, `tuple`
    *   `set`
    *   `dict` (removes key-value pairs)
    *   `str` (removes characters)
    *   `bytes`, `bytearray` (removes bytes)
    *   `int` (removes ~half the bits from binary representation)
    *   `float` (removes ~half the bits from IEEE 754 representation - **Warning:** may produce NaN/Inf/unexpected values)
    *   `bool`, `None` (returned unchanged)
*   **Python 3.8+**
*   **Type Hinted**

## Installation

Install directly from PyPI:

```bash
pip install thanospy
```

Or install from the source repository:

```bash
pip install git+https://github.com/manyan-chan/thanosPy.git # Update USERNAME/REPO
```

For local development:

```bash
git clone https://github.com/manyan-chan/thanosPy.git # Update USERNAME/REPO
cd thanosPy
pip install -e .[test]
```

## Usage Example

```python
import thanospy
import random

# For reproducibility in example
random.seed(42)

my_list = list(range(10))
print(f"Original List: {my_list}")
snapped_list = thanospy.snap(my_list)
print(f"Snapped List:  {snapped_list} (Length: {len(snapped_list)})")
# Example Output: Snapped List:  [0, 1, 3, 4, 7] (Length: 5)

my_tuple = tuple(range(1, 11))
print(f"\nOriginal Tuple: {my_tuple}")
snapped_tuple = thanospy.snap(my_tuple)
print(f"Snapped Tuple:  {snapped_tuple} (Length: {len(snapped_tuple)})")
# Example Output: Snapped Tuple:  (1, 2, 4, 5, 10) (Length: 5)

my_set = set(chr(ord('a') + i) for i in range(8))
print(f"\nOriginal Set: {my_set}")
snapped_set = thanospy.snap(my_set)
print(f"Snapped Set:  {snapped_set} (Length: {len(snapped_set)})")
# Example Output: Snapped Set:  {'g', 'a', 'd', 'b'} (Length: 4)

my_dict = {i: i*i for i in range(7)}
print(f"\nOriginal Dict: {my_dict}")
snapped_dict = thanospy.snap(my_dict)
print(f"Snapped Dict:  {snapped_dict} (Length: {len(snapped_dict)})")
# Example Output: Snapped Dict:  {0: 0, 5: 25, 3: 9, 1: 1} (Length: 4)

my_string = "abcdefghijklmnopqrstuvwxyz"
print(f"\nOriginal String: '{my_string}'")
snapped_string = thanospy.snap(my_string)
print(f"Snapped String:  '{snapped_string}' (Length: {len(snapped_string)})")
# Example Output: Snapped String:  'abcefhinopqsuwx' (Length: 13) # Corrected based on test seed

my_int = 1234567890
binary_int = bin(my_int)
print(f"\nOriginal Int: {my_int} ({binary_int})")
snapped_int = thanospy.snap(my_int)
binary_snapped_int = bin(snapped_int)
print(f"Snapped Int:  {snapped_int} ({binary_snapped_int})")
# Example Output: Snapped Int:  3345 (0b110100010001) # Corrected based on test seed

my_float = 123.456
print(f"\nOriginal Float: {my_float}")
snapped_float = thanospy.snap(my_float)
print(f"Snapped Float:  {snapped_float}")
# Example Output: Snapped Float:  -1.918078863119037e-178 (Results vary wildly!)

print(f"\nOriginal Bool: {True}")
print(f"Snapped Bool:  {thanospy.snap(True)}")
# Example Output: Snapped Bool:  True

print(f"\nOriginal None: {None}")
print(f"Snapped None:  {thanospy.snap(None)}")
# Example Output: Snapped None:  None

# Unsupported type
try:
    class Custom: pass
    thanospy.snap(Custom())
except TypeError as e:
    print(f"\nError for unsupported type: {e}")
# Example Output: Error for unsupported type: Unsupported data type for snap: CustomObject

```

## How Snapping Works

*   **Sequences/Sets/Dicts:** Randomly selects ~50% of the items/keys to *keep*. The number kept is `ceil(n / 2)`.
*   **Integers:** Converts the absolute value to its binary string representation (e.g., `10` -> `'1010'`). Randomly keeps `ceil(num_bits / 2)` bits. Converts the resulting binary string back to an integer. The original sign is reapplied.
*   **Floats:** Gets the IEEE 754 double-precision byte representation, converts to an integer, snaps the bits of that integer using the integer method, converts back to bytes, and then back to a float. **Warning:** This is a low-level manipulation and frequently results in very small numbers, `NaN`, `Infinity`, or `-Infinity`. Use with caution!
*   **Bool/None:** These types are returned unchanged as "snapping" doesn't apply meaningfully.

## Testing

The package uses `pytest`. To run tests:

1.  Install test dependencies: `pip install -e .[test]`
2.  Run from the root directory:

```bash
pytest
```

## Contributing

Contributions (bug reports, feature requests, PRs) are welcome! Please check the [GitHub Repository](https://github.com/manyan-chan/thanosPy).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.