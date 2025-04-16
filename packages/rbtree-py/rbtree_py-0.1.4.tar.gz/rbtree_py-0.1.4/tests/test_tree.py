# tests/test_tree.py
import random

import pytest

from redblacktree import BLACK, RedBlackTree


# Helper to verify RBT properties (optional but good for complex debugging)
# Note: Thorough property checking is complex. These are basic checks.
def _is_bst(node, tree, min_key, max_key):
    if node is tree.nil:
        return True
    # Ensure node.key is comparable
    if node.key is None:  # Should not happen for non-nil nodes
        return False
    if (min_key is not None and node.key <= min_key) or (
        max_key is not None and node.key >= max_key
    ):
        print(f"BST violation at Node {node.key}: min={min_key}, max={max_key}")
        return False
    # Type ignore needed as comparison works but type checker might complain depending on K
    return _is_bst(node.left, tree, min_key, node.key) and _is_bst(
        node.right, tree, node.key, max_key
    )  # type: ignore


def _check_bst_property(tree):
    """Check if the tree maintains the Binary Search Tree property."""
    return _is_bst(tree.root, tree, None, None)


def _check_red_property(node, tree):
    """Check Rule 4: If a node is red, then both its children are black."""
    if node is tree.nil:
        return True
    if node.is_red():
        # Check left child
        if node.left is not tree.nil and node.left.is_red():  # type: ignore
            print(
                f"Red violation at Node {node.key}: Parent Red, Left Child {node.left.key} Red"
            )  # type: ignore
            return False
        # Check right child
        if node.right is not tree.nil and node.right.is_red():  # type: ignore
            print(
                f"Red violation at Node {node.key}: Parent Red, Right Child {node.right.key} Red"
            )  # type: ignore
            return False
    # Recursively check children
    return _check_red_property(node.left, tree) and _check_red_property(
        node.right, tree
    )  # type: ignore


def _black_height(node, tree):
    """Calculate black-height, return -1 if RBT property 5 violated."""
    if node is tree.nil:
        return 1  # NIL nodes contribute 1 to black height

    left_bh = _black_height(node.left, tree)  # type: ignore
    right_bh = _black_height(node.right, tree)  # type: ignore

    # If recursive call detected violation, propagate it up
    if left_bh == -1 or right_bh == -1:
        return -1

    # Check if black heights of children are equal
    if left_bh != right_bh:
        print(
            f"Black height violation at Node {node.key}: Left BH={left_bh}, Right BH={right_bh}"
        )  # type: ignore
        return -1  # Violation detected

    # Calculate black height for this node
    increment = 1 if node.is_black() else 0
    return left_bh + increment  # Return black height of this subtree


def _check_black_height_property(tree):
    """Check Rule 5: All paths from root to leaves have the same black height."""
    # We only need to check if the black height calculation returns a valid height (-1 indicates violation)
    bh = _black_height(tree.root, tree)
    if bh == -1:
        print("Rule 5 Violation: Black height mismatch detected.")
        return False
    return True


def _check_rbt_properties(tree):
    """Run basic checks on RBT properties."""
    if tree.root is tree.nil:  # Handle empty tree case
        assert tree.nil.color == BLACK, "Rule 3 Violation: NIL must be black"
        return  # Empty tree trivially satisfies other properties

    assert tree.root.color == BLACK, "Rule 2 Violation: Root must be black"
    assert tree.nil.color == BLACK, "Rule 3 Violation: NIL must be black"
    assert _check_bst_property(tree), "BST Property Violation"
    assert _check_red_property(tree.root, tree), (
        "Rule 4 Violation: Red node has red child"
    )
    assert _check_black_height_property(tree), "Rule 5 Violation: Black height mismatch"


# --- Test Fixtures ---
@pytest.fixture
def empty_tree():
    return RedBlackTree[int, str]()


@pytest.fixture
def simple_tree():
    tree = RedBlackTree[int, str]()
    tree[10] = "A"
    tree[5] = "B"
    tree[15] = "C"
    _check_rbt_properties(tree)  # Ensure fixture itself is valid
    return tree


@pytest.fixture
def complex_tree():
    tree = RedBlackTree[int, int]()
    keys = list(range(20))
    random.shuffle(keys)
    for k in keys:
        tree[k] = k * 10
    _check_rbt_properties(tree)  # Ensure fixture itself is valid
    return tree


# --- Test Cases ---


def test_init_empty_tree(empty_tree):
    assert len(empty_tree) == 0
    assert empty_tree.root is empty_tree.nil
    assert empty_tree.minimum() is empty_tree.nil
    assert empty_tree.maximum() is empty_tree.nil
    _check_rbt_properties(empty_tree)


def test_insert_single_node(empty_tree):
    empty_tree[10] = "RootValue"
    assert len(empty_tree) == 1
    assert empty_tree.root is not empty_tree.nil
    assert empty_tree.root.key == 10
    assert empty_tree.root.value == "RootValue"
    assert empty_tree.root.color == BLACK  # Rule 2
    assert empty_tree.root.left is empty_tree.nil
    assert empty_tree.root.right is empty_tree.nil
    assert empty_tree.root.parent is empty_tree.nil
    _check_rbt_properties(empty_tree)


def test_insert_multiple_nodes(empty_tree):
    keys = [10, 5, 15, 3, 7, 12, 18]
    for i, k in enumerate(keys):
        empty_tree[k] = str(k)
        assert len(empty_tree) == i + 1
        _check_rbt_properties(empty_tree)  # Check properties after each insert

    assert len(empty_tree) == len(keys)
    assert list(empty_tree) == sorted(keys)  # Check iteration order


def test_insert_duplicates_updates_value(simple_tree):
    initial_len = len(simple_tree)
    assert simple_tree[10] == "A"
    simple_tree[10] = "UpdatedA"
    assert len(simple_tree) == initial_len  # Length should not change
    assert simple_tree[10] == "UpdatedA"
    _check_rbt_properties(simple_tree)


def test_search(simple_tree):
    node10 = simple_tree.search(10)
    assert node10 is not simple_tree.nil and node10.value == "A"
    node5 = simple_tree.search(5)
    assert node5 is not simple_tree.nil and node5.value == "B"
    node15 = simple_tree.search(15)
    assert node15 is not simple_tree.nil and node15.value == "C"
    assert simple_tree.search(99) is simple_tree.nil


def test_contains(simple_tree):
    assert 10 in simple_tree
    assert 5 in simple_tree
    assert 15 in simple_tree
    assert 99 not in simple_tree
    assert 0 not in simple_tree


def test_getitem(simple_tree):
    assert simple_tree[10] == "A"
    assert simple_tree[5] == "B"
    assert simple_tree[15] == "C"


def test_getitem_keyerror(simple_tree):
    with pytest.raises(KeyError):
        _ = simple_tree[99]


def test_minimum_maximum(simple_tree):
    simple_tree[3] = "D"
    simple_tree[18] = "E"
    min_node = simple_tree.minimum()
    max_node = simple_tree.maximum()
    assert min_node is not simple_tree.nil
    assert min_node.key == 3
    assert min_node.value == "D"
    assert max_node is not simple_tree.nil
    assert max_node.key == 18
    assert max_node.value == "E"
    _check_rbt_properties(simple_tree)


def test_minimum_maximum_empty(empty_tree):
    assert empty_tree.minimum() is empty_tree.nil
    assert empty_tree.maximum() is empty_tree.nil


def test_iteration(complex_tree):
    expected_keys = sorted(list(range(20)))
    assert list(complex_tree) == expected_keys
    assert list(complex_tree.values()) == [k * 10 for k in expected_keys]
    assert list(complex_tree.items()) == [(k, k * 10) for k in expected_keys]


def test_delete_leaf_node(simple_tree):
    # Add a few more leaves
    simple_tree[3] = "D"
    simple_tree[7] = "E"
    simple_tree[12] = "F"
    simple_tree[18] = "G"
    initial_len = len(simple_tree)  # Should be 7
    _check_rbt_properties(simple_tree)

    # Delete leaf 3
    del simple_tree[3]
    assert len(simple_tree) == initial_len - 1
    assert 3 not in simple_tree
    assert list(simple_tree) == [5, 7, 10, 12, 15, 18]
    _check_rbt_properties(simple_tree)

    # Delete leaf 18
    del simple_tree[18]
    assert len(simple_tree) == initial_len - 2
    assert 18 not in simple_tree
    assert list(simple_tree) == [5, 7, 10, 12, 15]
    _check_rbt_properties(simple_tree)

    # Delete leaf 7
    del simple_tree[7]
    assert len(simple_tree) == initial_len - 3
    assert 7 not in simple_tree
    assert list(simple_tree) == [5, 10, 12, 15]
    _check_rbt_properties(simple_tree)

    # Delete leaf 12
    del simple_tree[12]
    assert len(simple_tree) == initial_len - 4
    assert 12 not in simple_tree
    assert list(simple_tree) == [5, 10, 15]
    _check_rbt_properties(simple_tree)


def test_delete_node_with_one_child(simple_tree):
    simple_tree[3] = "D"  # Left child of 5
    initial_len = len(simple_tree)  # 4
    _check_rbt_properties(simple_tree)

    # Delete node 5 which has one left child (3)
    del simple_tree[5]
    assert len(simple_tree) == initial_len - 1
    assert 5 not in simple_tree
    assert 3 in simple_tree
    assert list(simple_tree) == [3, 10, 15]
    _check_rbt_properties(simple_tree)

    # Reset and test one right child
    tree = RedBlackTree[int, str]()
    tree[10] = "A"
    tree[5] = "B"
    tree[15] = "C"
    tree[18] = "D"  # Right child of 15
    initial_len = len(tree)  # 4
    _check_rbt_properties(tree)

    # Delete node 15 which has one right child (18)
    del tree[15]
    assert len(tree) == initial_len - 1
    assert 15 not in tree
    assert 18 in tree
    assert list(tree) == [5, 10, 18]
    _check_rbt_properties(tree)


def test_delete_node_with_two_children(simple_tree):
    # simple_tree has 5, 10, 15
    simple_tree[3] = "D"
    simple_tree[7] = "E"
    simple_tree[12] = "F"
    simple_tree[18] = "G"
    # Tree keys: 3, 5, 7, 10, 12, 15, 18
    initial_len = len(simple_tree)  # 7
    _check_rbt_properties(simple_tree)

    # Delete root node 10 (two children: 5 and 15)
    # Its successor is 12
    del simple_tree[10]
    assert len(simple_tree) == initial_len - 1
    assert 10 not in simple_tree
    # Root should become black (successor 12 might have been red or black)
    assert simple_tree.root.color == BLACK if len(simple_tree) > 0 else True
    assert list(simple_tree) == [3, 5, 7, 12, 15, 18]  # Check order preserved
    _check_rbt_properties(simple_tree)  # Check properties maintained

    # Now delete node 5 (two children: 3 and 7)
    # Successor is 7
    del simple_tree[5]
    assert len(simple_tree) == initial_len - 2
    assert 5 not in simple_tree
    assert simple_tree.root.color == BLACK if len(simple_tree) > 0 else True
    assert list(simple_tree) == [3, 7, 12, 15, 18]
    _check_rbt_properties(simple_tree)

    # Now delete node 15 (two children: 12(now left child) and 18)
    # Successor is 18
    del simple_tree[15]
    assert len(simple_tree) == initial_len - 3
    assert 15 not in simple_tree
    assert simple_tree.root.color == BLACK if len(simple_tree) > 0 else True
    assert list(simple_tree) == [3, 7, 12, 18]
    _check_rbt_properties(simple_tree)


def test_delete_root_node_repeatedly(simple_tree):
    simple_tree[3] = "D"
    simple_tree[7] = "E"
    simple_tree[12] = "F"
    simple_tree[18] = "G"
    initial_len = len(simple_tree)  # 7
    _check_rbt_properties(simple_tree)

    # Delete root until tree is empty
    for i in range(initial_len):
        root_key = simple_tree.root.key
        assert root_key is not None  # Root should not be nil if len > 0
        del simple_tree[root_key]
        assert root_key not in simple_tree
        assert len(simple_tree) == initial_len - (i + 1)
        if len(simple_tree) > 0:
            _check_rbt_properties(simple_tree)
        else:
            assert simple_tree.root is simple_tree.nil

    assert len(simple_tree) == 0
    assert list(simple_tree) == []
    _check_rbt_properties(simple_tree)  # Check empty tree properties


def test_delete_keyerror(simple_tree):
    with pytest.raises(KeyError):
        del simple_tree[99]
    with pytest.raises(KeyError):  # Try deleting again after it's gone
        del simple_tree[10]
        del simple_tree[10]


def test_delete_from_empty_tree(empty_tree):
    with pytest.raises(KeyError):
        del empty_tree[10]


def test_complex_insert_delete_stress(complex_tree):
    # Start with 20 nodes (0-19) from fixture
    assert len(complex_tree) == 20
    _check_rbt_properties(complex_tree)
    initial_keys = set(range(20))

    # Delete 10 random nodes
    keys_to_delete = set(random.sample(list(initial_keys), 10))
    remaining_keys = sorted(list(initial_keys - keys_to_delete))
    for key in keys_to_delete:
        del complex_tree[key]
        assert key not in complex_tree
        _check_rbt_properties(complex_tree)  # Check after each delete

    assert len(complex_tree) == 10
    assert list(complex_tree) == remaining_keys

    # Insert 10 new nodes and re-insert 5 deleted ones
    new_keys = set(random.sample(range(20, 40), 10))
    reinsert_keys = set(random.sample(list(keys_to_delete), 5))
    keys_to_add = list(new_keys | reinsert_keys)
    random.shuffle(keys_to_add)

    final_keys_set = set(remaining_keys) | set(keys_to_add)
    final_keys_sorted = sorted(list(final_keys_set))

    for key in keys_to_add:
        complex_tree[key] = key * 100
        _check_rbt_properties(complex_tree)  # Check after each insert

    assert len(complex_tree) == len(final_keys_set)  # Should be 10 + 10 + 5 = 25
    assert list(complex_tree) == final_keys_sorted
    _check_rbt_properties(complex_tree)


def test_delete_all_nodes_random_order():
    tree = RedBlackTree[int, int]()
    n = 50
    keys = list(range(n))
    random.shuffle(keys)
    for k in keys:
        tree[k] = k

    assert len(tree) == n
    _check_rbt_properties(tree)

    keys_to_delete = list(range(n))
    random.shuffle(keys_to_delete)

    for i, k in enumerate(keys_to_delete):
        # Optional: print state before deletion for debugging failures
        # print(f"Deleting {k}, len={len(tree)}")
        # tree.print_tree()
        del tree[k]
        assert k not in tree
        assert len(tree) == n - (i + 1)
        if len(tree) > 0:
            _check_rbt_properties(tree)  # Check rigorously
        else:
            assert tree.root is tree.nil

    assert len(tree) == 0
    assert tree.root is tree.nil
    _check_rbt_properties(tree)  # Check empty tree properties


def test_large_number_of_insertions():
    tree = RedBlackTree[int, int]()
    n = 1000
    keys = list(range(n))
    random.shuffle(keys)
    for i, k in enumerate(keys):
        tree[k] = k * 2
        # Check properties periodically, not necessarily on every insert for speed
        if (i + 1) % 100 == 0 or i == n - 1:
            assert len(tree) == i + 1
            _check_rbt_properties(tree)

    assert len(tree) == n
    assert list(tree) == list(range(n))
    _check_rbt_properties(tree)


def test_tree_with_non_numeric_keys():
    tree = RedBlackTree[str, int]()
    tree["apple"] = 1
    tree["banana"] = 2
    tree["cherry"] = 3
    tree["date"] = 4
    tree["fig"] = 5

    assert len(tree) == 5
    _check_rbt_properties(tree)
    expected_keys = ["apple", "banana", "cherry", "date", "fig"]
    assert list(tree) == expected_keys
    assert tree["banana"] == 2
    assert "grape" not in tree

    del tree["cherry"]
    assert len(tree) == 4
    assert "cherry" not in tree
    expected_keys.remove("cherry")
    assert list(tree) == expected_keys
    _check_rbt_properties(tree)

    tree["grape"] = 6
    assert len(tree) == 5
    expected_keys.append("grape")
    expected_keys.sort()
    assert list(tree) == expected_keys
    _check_rbt_properties(tree)

    del tree["apple"]
    del tree["fig"]
    assert len(tree) == 3
    expected_keys.remove("apple")
    expected_keys.remove("fig")
    assert list(tree) == expected_keys
    _check_rbt_properties(tree)
