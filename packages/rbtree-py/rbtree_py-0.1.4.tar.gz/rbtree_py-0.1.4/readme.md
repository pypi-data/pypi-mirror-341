# Python Red-Black Tree (rbtree-py)

[![PyPI version](https://badge.fury.io/py/rbtree-py.svg)](https://badge.fury.io/py/rbtree-py) <!-- Placeholder: Update link if/when published -->
[![CI Status](https://github.com/manyan-chan/rbtree-py/actions/workflows/python-package.yml/badge.svg)](https://github.com/manyan-chan/rbtree-py/actions/workflows/python-package.yml) <!-- Update USERNAME/REPO -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Versions](https://img.shields.io/pypi/pyversions/rbtree-py.svg) <!-- Placeholder -->

A pure Python implementation of a Red-Black Tree, a self-balancing binary search tree. This data structure provides efficient insertion, deletion, and search operations in O(log n) time complexity.

## Features

*   **Key-Value Storage:** Stores data similar to a dictionary.
*   **Efficient Operations:** `insert`, `delete`, `search`, `minimum`, `maximum` all operate in O(log n) time.
*   **Ordered Iteration:** Iterate through keys, values, or items (key-value pairs) in ascending key order.
*   **Standard Dictionary Interface:** Supports `len()`, `in`, `[]` (getitem), `[]=` (setitem), `del []` (delitem).
*   **Type Hinting:** Fully type-hinted for better static analysis and developer experience.
*   **Python 3.8+:** Compatible with modern Python versions.

## Installation

You can install the package directly from PyPI (once published):

```bash
pip install rbtree-py
```

Or, install directly from the source repository:

```bash
pip install git+https://github.com/manyan-chan/rbtree-py.git
```

For local development, clone the repository and install in editable mode:

```bash
git clone https://github.com/manyan-chan/rbtree-py.git
cd rbtree-py
pip install -e .[test]
```

## Usage

Here's a basic example of how to use the `RedBlackTree`:

```python
from redblacktree import RedBlackTree

# Create a new tree
rbt = RedBlackTree[int, str]() # Specify key and value types (optional but recommended)

# Insert key-value pairs (like a dictionary)
rbt[10] = "Apple"
rbt[5] = "Banana"
rbt[15] = "Cherry"
rbt[3] = "Date"
rbt[7] = "Elderberry"
rbt[12] = "Fig"
rbt[18] = "Grape"

# Check length
print(f"Tree size: {len(rbt)}") # Output: Tree size: 7

# Check if a key exists
print(f"Has key 7? {7 in rbt}")   # Output: Has key 7? True
print(f"Has key 99? {99 in rbt}") # Output: Has key 99? False

# Get value by key
print(f"Value for key 15: {rbt[15]}") # Output: Value for key 15: Cherry

# Attempt to get non-existent key (raises KeyError)
try:
    print(rbt[99])
except KeyError as e:
    print(e) # Output: 'Key not found: 99'

# Update value
rbt[5] = "Blueberry"
print(f"Updated value for key 5: {rbt[5]}") # Output: Updated value for key 5: Blueberry

# Delete a key
del rbt[12]
print(f"Tree size after deleting 12: {len(rbt)}") # Output: Tree size after deleting 12: 6
print(f"Has key 12? {12 in rbt}") # Output: Has key 12? False

# Iterate over keys (sorted order)
print("Keys:", list(rbt)) # Output: Keys: [3, 5, 7, 10, 15, 18]

# Iterate over values (sorted by key)
print("Values:", list(rbt.values())) # Output: Values: ['Date', 'Blueberry', 'Elderberry', 'Apple', 'Cherry', 'Grape']

# Iterate over items (key, value) pairs (sorted by key)
print("Items:", list(rbt.items()))
# Output: Items: [(3, 'Date'), (5, 'Blueberry'), (7, 'Elderberry'), (10, 'Apple'), (15, 'Cherry'), (18, 'Grape')]

# Find minimum and maximum keys
min_node = rbt.minimum()
max_node = rbt.maximum()
if min_node is not rbt.nil: # Check if tree is not empty
     print(f"Minimum key: {min_node.key}, Value: {min_node.value}")
if max_node is not rbt.nil:
     print(f"Maximum key: {max_node.key}, Value: {max_node.value}")
# Output:
# Minimum key: 3, Value: Date
# Maximum key: 18, Value: Grape

# Print tree structure (for debugging)
# print("\nTree Structure:")
# rbt.print_tree() # Optional: Visualize the tree structure

```

## Testing

The package uses `pytest` for testing. To run the tests:

1.  Make sure you have installed the test dependencies: `pip install -e .[test]`
2.  Run pytest from the root directory:

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Add tests for your changes.
5.  Ensure all tests pass (`pytest`).
6.  Format your code (e.g., using `black` or `flake8`).
7.  Commit your changes (`git commit -am 'Add some feature'`).
8.  Push to the branch (`git push origin feature/your-feature-name`).
9.  Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.