# redblacktree/tree.py
from typing import Generator, Generic, Optional, Tuple, TypeVar, cast

# Define type variables for keys and values
K = TypeVar("K")
V = TypeVar("V")

# --- Constants ---
RED = "RED"
BLACK = "BLACK"


# --- Node Class ---
class RBNode(Generic[K, V]):
    """Represents a node in the Red-Black Tree."""

    # Declare attributes for clarity
    key: Optional[K]
    value: Optional[V]
    color: str
    parent: "RBNode[K, V]"  # Parent should always point to another node or nil
    left: "RBNode[K, V]"  # Left should always point to another node or nil
    right: "RBNode[K, V]"  # Right should always point to another node or nil

    def __init__(
        self,
        key: Optional[K],
        value: Optional[V],
        color: str = RED,
        parent: Optional["RBNode[K, V]"] = None,  # Allow None initially for nil setup
        left: Optional["RBNode[K, V]"] = None,  # Allow None initially for nil setup
        right: Optional["RBNode[K, V]"] = None,
    ):  # Allow None initially for nil setup
        self.key = key
        self.value = value
        self.color = color
        # Initial assignment, will be overwritten by sentinel logic later
        self.parent = parent if parent is not None else self  # type: ignore # Temp assignment
        self.left = left if left is not None else self  # type: ignore # Temp assignment
        self.right = right if right is not None else self  # type: ignore # Temp assignment

    def __repr__(self) -> str:
        key_repr = repr(self.key) if self.key is not None else "None"
        value_repr = repr(self.value) if self.value is not None else "None"
        return f"RBNode({key_repr}, {value_repr}, {self.color})"

    def is_black(self) -> bool:
        return self.color == BLACK

    def is_red(self) -> bool:
        return self.color == RED


# --- RedBlackTree Class ---
class RedBlackTree(Generic[K, V]):
    """
    A Red-Black Tree implementation supporting key-value pairs.
    """

    # Type hint for nil needs careful consideration.
    # It acts like RBNode[K,V] but holds None.
    # Using RBNode[Any, Any] or suppressing type checks might be needed.
    # Let's try RBNode[K, V] and use casts.
    nil: RBNode[K, V]
    root: RBNode[K, V]
    _count: int

    def __init__(self):
        # Create the sentinel node
        # Cast needed because K/V are initially None, violating invariance
        _nil_node = RBNode(key=None, value=None, color=BLACK)
        _nil_node.parent = _nil_node
        _nil_node.left = _nil_node
        _nil_node.right = _nil_node
        self.nil = cast(
            RBNode[K, V], _nil_node
        )  # Cast the concrete nil to generic type

        # Root initially points to the sentinel
        self.root = self.nil
        self._count = 0

    def __len__(self) -> int:
        """Return the number of nodes in the tree."""
        return self._count

    def __contains__(self, key: K) -> bool:
        """Check if a key exists in the tree (e.g., `key in tree`)."""
        return self.search(key) is not self.nil

    def __getitem__(self, key: K) -> V:
        """Get the value associated with a key (e.g., `tree[key]`)."""
        node = self.search(key)
        if node is self.nil:
            raise KeyError(f"Key not found: {key}")
        # Node is not nil, so value should be V, not None
        assert node.value is not None
        return node.value

    def __setitem__(self, key: K, value: V) -> None:
        """Insert or update a key-value pair (e.g., `tree[key] = value`)."""
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        """Delete a key-value pair (e.g., `del tree[key]`)."""
        node = self.search(key)
        if node is self.nil:
            raise KeyError(f"Key not found: {key}")
        # search guarantees node is not nil if exception wasn't raised
        self.delete(node)

    def __iter__(self) -> Generator[K, None, None]:
        """Iterate over keys in ascending order."""
        yield from self._inorder_walk_keys(self.root)

    def items(self) -> Generator[Tuple[K, V], None, None]:
        """Iterate over (key, value) pairs in ascending order."""
        yield from self._inorder_walk_items(self.root)

    def values(self) -> Generator[V, None, None]:
        """Iterate over values in ascending key order."""
        for _, value in self.items():
            yield value

    # --- Search ---
    def search(self, key: K) -> RBNode[K, V]:
        """Search for a node with the given key."""
        node = self.root
        while node is not self.nil:
            assert node.key is not None  # Key must exist if node is not nil
            if key == node.key:
                return node
            # Assume keys are comparable. Type ignores needed if K isn't constrained.
            if key < node.key:  # type: ignore[operator]
                node = node.left
            else:
                node = node.right
        # Returns self.nil if not found
        return self.nil  # Type checker knows self.nil is RBNode[K, V] now

    # --- Minimum and Maximum ---
    def minimum(self, node: Optional[RBNode[K, V]] = None) -> RBNode[K, V]:
        """Find the node with the minimum key in the subtree rooted at `node`."""
        current = node if node is not None else self.root
        if current is self.nil:
            return self.nil  # Return sentinel for empty tree

        while current.left is not self.nil:
            current = current.left
        return current

    def maximum(self, node: Optional[RBNode[K, V]] = None) -> RBNode[K, V]:
        """Find the node with the maximum key in the subtree rooted at `node`."""
        current = node if node is not None else self.root
        if current is self.nil:
            return self.nil  # Return sentinel for empty tree

        while current.right is not self.nil:
            current = current.right
        return current

    # --- Rotations ---
    def _left_rotate(self, x: RBNode[K, V]):
        """Perform a left rotation on node x."""
        y = x.right
        if y is self.nil:
            return  # Cannot rotate if right child is nil

        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:  # x is x.parent.right
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y: RBNode[K, V]):
        """Perform a right rotation on node y."""
        x = y.left
        if x is self.nil:
            return  # Cannot rotate if left child is nil

        y.left = x.right
        if x.right is not self.nil:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is self.nil:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:  # y is y.parent.left
            y.parent.left = x

        x.right = y
        y.parent = x

    # --- Insertion ---
    def insert(self, key: K, value: V):
        """Insert a new key-value pair into the tree."""
        existing_node = self.search(key)
        if existing_node is not self.nil:
            # Update value if key exists
            existing_node.value = value
            return

        # Find parent for new node (Standard BST insert)
        parent_node = self.nil
        current_node = self.root
        while current_node is not self.nil:
            parent_node = current_node
            assert current_node.key is not None  # Key exists if not nil
            if key < current_node.key:  # type: ignore[operator]
                current_node = current_node.left
            else:
                current_node = current_node.right

        # Create the new node
        # parent_node is guaranteed not None here unless tree was empty
        # parent_node points to nil if tree was empty
        new_node = RBNode(
            key, value, color=RED, parent=parent_node, left=self.nil, right=self.nil
        )
        self._count += 1

        if parent_node is self.nil:
            self.root = new_node  # Tree was empty
        elif new_node.key < parent_node.key:  # type: ignore[operator] # parent_node cannot be nil here
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        # Fix Red-Black Tree properties starting from the new node
        self._insert_fixup(new_node)

    def _insert_fixup(self, z: RBNode[K, V]):
        """Maintain Red-Black Tree properties after insertion."""
        # Loop invariant: z is RED.
        # Loop condition: z's parent is RED (violating Rule 4).
        while (
            z.parent.is_red()
        ):  # Implicitly checks z.parent is not nil (root parent is nil)
            # If parent is red, it cannot be the root, so grandparent must exist.
            parent = z.parent
            assert parent is not self.nil  # Parent is red, cannot be nil
            grandparent = parent.parent
            assert (
                grandparent is not self.nil
            )  # Parent is red -> not root -> has parent

            if parent is grandparent.left:
                uncle = grandparent.right
                if uncle.is_red():  # Case 1: Uncle is RED
                    parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    z = grandparent  # Move up and continue check
                else:  # Uncle is BLACK (or nil)
                    if z is parent.right:  # Case 2: z is right child (triangle)
                        z = parent
                        self._left_rotate(z)
                        # After rotation, z is now the lower node, need parent/grandparent again
                        parent = z.parent  # z might have changed, re-get parent
                        assert (
                            parent is not self.nil
                        )  # Should exist after rotation if z wasn't root
                        grandparent = parent.parent
                        assert grandparent is not self.nil  # Should also exist

                    # Case 3: z is left child (line) - or after Case 2 reduction
                    # Ensure parent/grandparent are valid before setting color
                    assert parent is not self.nil
                    assert grandparent is not self.nil
                    parent.color = BLACK
                    grandparent.color = RED
                    self._right_rotate(grandparent)
            else:  # Symmetric case: parent is grandparent.right
                uncle = grandparent.left
                if uncle.is_red():  # Case 1
                    parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    z = grandparent
                else:  # Uncle is BLACK (or nil)
                    if z is parent.left:  # Case 2 (triangle)
                        z = parent
                        self._right_rotate(z)
                        # Re-get parent/grandparent
                        parent = z.parent
                        assert parent is not self.nil
                        grandparent = parent.parent
                        assert grandparent is not self.nil

                    # Case 3 (line)
                    assert parent is not self.nil
                    assert grandparent is not self.nil
                    parent.color = BLACK
                    grandparent.color = RED
                    self._left_rotate(grandparent)

            # Break if z reached the root (which will be colored black at the end)
            if z is self.root:
                break

        # Rule 2: Ensure root is always black
        self.root.color = BLACK

    # --- Deletion ---
    def _transplant(self, u: RBNode[K, V], v: RBNode[K, V]):
        """Replace subtree rooted at u with subtree rooted at v."""
        if u.parent is self.nil:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:  # u is u.parent.right
            u.parent.right = v

        # Important: Set parent pointer for v ONLY if v is not the sentinel
        if v is not self.nil:
            v.parent = u.parent

    def delete(self, z: RBNode[K, V]):
        """Delete node z from the tree."""
        if z is self.nil:
            return  # Should not happen if called from __delitem__

        y = z  # Node to potentially splice out or move
        y_original_color = y.color
        x: RBNode[K, V]  # Node that moves into y's original position
        x_parent: RBNode[K, V]  # Parent of x's position after deletion/transplant

        if z.left is self.nil:
            x = z.right
            x_parent = z.parent  # Original parent of z
            self._transplant(z, x)
        elif z.right is self.nil:
            x = z.left
            x_parent = z.parent  # Original parent of z
            self._transplant(z, x)
        else:  # z has two children
            y = self.minimum(z.right)  # y is z's successor
            y_original_color = y.color
            x = y.right  # x is y's right child (can be nil)

            if y.parent is z:
                # Case 3a: y is direct child of z. x replaces y.
                # x's parent *context* for fixup is y itself.
                x_parent = y
            else:
                # Case 3b: y is not direct child. x replaces y first.
                # x's parent *context* for fixup is y's original parent.
                x_parent = y.parent
                self._transplant(y, x)  # x takes y's place
                y.right = z.right  # y adopts z's right subtree
                y.right.parent = y

            # Now, transplant y into z's position
            self._transplant(z, y)  # y takes z's place
            y.left = z.left  # y adopts z's left subtree
            y.left.parent = y
            y.color = z.color  # y gets z's color

            # If y was z's child (Case 3a), and x moved into y's spot,
            # x's actual parent is now y. The transplant of x already set this if x is not nil.
            # x_parent = y remains the correct *context* for the fixup initiation.

        self._count -= 1

        # If a black node was removed (or moved from a black position),
        # fix potential violations starting from node x.
        if y_original_color == BLACK:
            # Ensure x_parent is valid (should be nil only if original z was root)
            # The transplant logic ensures x_parent points to the correct node or self.nil
            self._delete_fixup(x, x_parent)

    def _delete_fixup(self, x: RBNode[K, V], x_parent: RBNode[K, V]):
        """Maintain Red-Black Tree properties after deletion of a black node."""
        # x is the node starting the fixup (can be nil, carries "extra black").
        # x_parent is the parent of x's position in the tree (cannot be None, only self.nil).

        while x is not self.root and x.is_black():
            # If x_parent is nil, x must be the root, loop condition fails.
            assert x_parent is not self.nil  # Parent must exist if x is not root

            if x is x_parent.left:
                sibling = x_parent.right
                assert (
                    sibling is not self.nil
                )  # Should exist if black height unbalanced

                if sibling.is_red():  # Case 1: Red sibling
                    sibling.color = BLACK
                    x_parent.color = RED
                    self._left_rotate(x_parent)
                    sibling = x_parent.right  # New sibling must be black

                # Now sibling is guaranteed BLACK (or loop would have terminated/rotated)
                assert sibling is not self.nil  # Should still exist

                # Case 2: Black sibling with two black children
                if sibling.left.is_black() and sibling.right.is_black():
                    sibling.color = RED
                    x = x_parent  # Move up the extra blackness
                    x_parent = x.parent  # Update parent context
                else:
                    # Case 3: Black sibling, left child red, right child black
                    if sibling.right.is_black():
                        # Ensure left child exists before coloring
                        if sibling.left is not self.nil:
                            sibling.left.color = BLACK
                        sibling.color = RED
                        self._right_rotate(sibling)
                        sibling = x_parent.right  # Update sibling after rotation

                    # Case 4: Black sibling, right child red
                    assert sibling is not self.nil  # Should exist
                    sibling.color = x_parent.color  # Transfer parent color
                    x_parent.color = BLACK
                    # Ensure right child exists before coloring
                    if sibling.right is not self.nil:
                        sibling.right.color = BLACK
                    self._left_rotate(x_parent)
                    x = self.root  # Fixup finished, terminate loop
            else:  # Symmetric case: x is x_parent.right
                sibling = x_parent.left
                assert sibling is not self.nil

                if sibling.is_red():  # Case 1
                    sibling.color = BLACK
                    x_parent.color = RED
                    self._right_rotate(x_parent)
                    sibling = x_parent.left  # New sibling must be black

                assert sibling is not self.nil

                # Case 2
                if sibling.right.is_black() and sibling.left.is_black():
                    sibling.color = RED
                    x = x_parent
                    x_parent = x.parent
                else:
                    # Case 3
                    if sibling.left.is_black():
                        if sibling.right is not self.nil:
                            sibling.right.color = BLACK
                        sibling.color = RED
                        self._left_rotate(sibling)
                        sibling = x_parent.left  # Update sibling

                    # Case 4
                    assert sibling is not self.nil
                    sibling.color = x_parent.color
                    x_parent.color = BLACK
                    if sibling.left is not self.nil:
                        sibling.left.color = BLACK
                    self._right_rotate(x_parent)
                    x = self.root  # Fixup finished

        # If x absorbed the extra black, ensure it's black.
        # If loop terminated because x became root, root must be black.
        if x is not self.nil:
            x.color = BLACK

    # --- Traversal Methods (Internal) ---
    def _inorder_walk_keys(self, node: RBNode[K, V]) -> Generator[K, None, None]:
        """Helper for inorder key iteration."""
        if node is not self.nil:
            yield from self._inorder_walk_keys(node.left)
            # Only yield if the key is not None (i.e., not the sentinel node)
            if node.key is not None:
                # We know key is K if not None
                yield node.key
            yield from self._inorder_walk_keys(node.right)

    def _inorder_walk_items(
        self, node: RBNode[K, V]
    ) -> Generator[Tuple[K, V], None, None]:
        """Helper for inorder item iteration."""
        if node is not self.nil:
            yield from self._inorder_walk_items(node.left)
            if node.key is not None:
                # Key and Value should be K/V if Key is not None
                assert node.value is not None
                yield (node.key, node.value)
            yield from self._inorder_walk_items(node.right)

    # --- Helper for Debugging (Optional) ---
    def print_tree(
        self, node: Optional[RBNode[K, V]] = None, indent: str = "", last: bool = True
    ):
        """Prints a structured representation of the tree (for debugging)."""
        if node is None:
            node = self.root

        if node is not self.nil:
            print(indent, end="")
            if last:
                print("R---- ", end="")
                indent += "     "
            else:
                print("L---- ", end="")
                indent += "|    "

            color_char = "R" if node.color == RED else "B"
            # Parent representation needs to handle nil correctly
            parent_key_repr = "NIL_SENTINEL"
            if node.parent is not self.nil:
                parent_key_repr = repr(
                    node.parent.key
                )  # Parent key could be None if parent is nil? No.

            print(f"{node.key!r}({color_char}, P:{parent_key_repr})")

            self.print_tree(node.left, indent, False)
            self.print_tree(node.right, indent, True)
