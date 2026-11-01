---
title: PyDTree — Build an Adaptive 20-Questions Engine
week: 4
category: Trees
start: 2026-10-23
end: 2026-11-08
---

**File to Submit:** `pydtree.py`  
**Language:** Python 3 (built-in standard library only)  
**Run Tests:** `python pydtree.py --test`  
**Play Mode:** `python pydtree.py`

---

## 📌 Submission

1. Ensure your code is placed inside your student directory: `students/<registration-no>/week4/pydtree.py`.
2. Do not import external third-party libraries (no `pip install` packages; standard `json`, `sys`, and `typing` only).
3. Open a pull request from your fork to `main` on or before **8 Nov 2026**. Touch only your own folder.

---

## 💡 A Quick Note Before You Begin: Why Solve This Yourself?

> In 1960, legendary computer scientist Donald Michie built _MENACE_ (Matchbox Educable Noughts and Crosses Engine) — a machine made entirely of 304 matchboxes that learned how to play Tic-Tac-Toe. It had no silicon microchips, no neural networks, and no cloud computing. It was purely a physical **decision tree** that mutated its branches through experience.
>
> Solving this yourself gives you one of the sweetest moments in programming: **watching a tree structure that YOU designed sit in your terminal, ask you questions, get something wrong, and literally grow a new branch in real-time memory to become smarter.**
>
> When you trace pointer grafting by hand and see your own recursive functions calculate heights and traversals effortlessly, you aren't just completing homework — you are mastering the exact non-linear mental model that powers file systems, abstract syntax trees (compilers), DOM engines, and machine learning decision forests.
>
> Follow the milestones below. Test each function as you go using `python pydtree.py --test`.

---

## 🧠 The Big Picture: Escaping the Linear Trap

In **Lab 1**, arrays forced us to shift elements in $O(n)$ time just to open a slot.  
In **Lab 2**, linked lists freed us from contiguous memory, but finding an item still meant walking node-by-node down a single corridor in $O(n)$ time.  
In **Lab 3**, queues and stacks managed arrivals and departures strictly at endpoints.

A **Tree** is our escape from the one-dimensional line. Instead of pointing to just one successor, every node can branch into multiple possibilities:

```text
               [Does it live in water?]
                     /          \
             (Yes)  /            \ (No)
                   v              v
              [Dolphin]      [Does it bark?]
                                /        \
                        (Yes)  /          \ (No)
                              v            v
                            [Dog]      [Elephant]
```

Notice the key insight:

- **Internal Nodes** contain **Questions** (Tests).
- **Leaf Nodes** contain **Answers** (Guesses).
- Every step down a binary branch eliminates half of the remaining universe!

---

## 🛠️ What to Build (Step by Step)

All your code goes inside `pydtree.py`.

### Milestone 1: The Decision Tree Node (`TreeNode`)

A node holds text, a `yes_child` pointer, and a `no_child` pointer:

```python
class TreeNode:
    def __init__(self, text: str, yes_child=None, no_child=None):
        self.text = text.strip()
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self) -> bool:
        """Returns True if this node has no children (it's a final guess)."""
        return self.yes_child is None and self.no_child is None
```

---

### Milestone 2: Recursive Metrics (`count_nodes`, `count_leaves`, `tree_height`)

Trees are recursive structures by nature (a tree is a root node connected to smaller subtrees). Write these three fundamental recursive functions:

1. `count_nodes(root)`:
   - Base case: If `root is None`, return `0`.
   - Recursive step: Return `1 + count_nodes(root.yes_child) + count_nodes(root.no_child)`.
2. `count_leaves(root)`:
   - Base case: If `root is None`, return `0`.
   - Leaf case: If `root.is_leaf()`, return `1`.
   - Recursive step: Return `count_leaves(root.yes_child) + count_leaves(root.no_child)`.
3. `tree_height(root)`:
   - Empty tree: Return `-1`.
   - Leaf node: Return `0`.
   - Recursive step: Return `1 + max(tree_height(root.yes_child), tree_height(root.no_child))`.

---

### Milestone 3: The 3 Great Recursive Walks (`preorder`, `inorder`, `postorder`)

Traversals define how we visit every node in a non-linear hierarchy:

- **Pre-order (`preorder_traversal`)**: `[Root] -> Left Subtree -> Right Subtree`.  
  _Application:_ Serializing and printing the tree from top to bottom.
- **In-order (`inorder_traversal`)**: `Left Subtree -> [Root] -> Right Subtree`.  
  _Application:_ In Binary Search Trees, in-order always returns items in sorted order!
- **Post-order (`postorder_traversal`)**: `Left Subtree -> Right Subtree -> [Root]`.  
  _Application:_ Bottom-up calculation (e.g. folder disk size, tree destruction, expression evaluation).

Each function should return a list of strings: `List[str]`.

---

### Milestone 4: Knowledge Tree Serialization (`tree_to_dict` & `dict_to_tree`)

To ensure your game remembers what it learned even after you exit the terminal, serialize the tree into JSON:

- `tree_to_dict(root)`:
  - If leaf: return `{"guess": root.text}`.
  - If question: return `{"question": root.text, "yes": tree_to_dict(root.yes_child), "no": tree_to_dict(root.no_child)}`.
- `dict_to_tree(data)`:
  - Inverse recursive function: recreates `TreeNode` objects from a nested dictionary.

---

### Milestone 5: The Magic of Pointer Grafting (`graft_new_knowledge`)

This is the single most important function in the assignment. When the computer makes an incorrect guess on a leaf node, you must transform that leaf into a question node in place!

```python
def graft_new_knowledge(
    leaf_node: TreeNode,
    new_question: str,
    new_guess: str,
    new_guess_is_yes: bool,
) -> None:
```

**How it works:**

1. Remember the old guess: `old_guess = leaf_node.text`.
2. Create two new leaves: `TreeNode(new_guess)` and `TreeNode(old_guess)`.
3. Mutate `leaf_node.text` to become the new distinguishing question.
4. Hook the children:
   - If `new_guess_is_yes == True`:
     - `leaf_node.yes_child = TreeNode(new_guess)`
     - `leaf_node.no_child = TreeNode(old_guess)`
   - Else:
     - `leaf_node.yes_child = TreeNode(old_guess)`
     - `leaf_node.no_child = TreeNode(new_guess)`

Notice: No arrays were resized, no elements were shifted. Just two pointer assignments!

---

### Milestone 6: Terminal ASCII Visualizer & Interactive REPL

Implement:

- `print_ascii_tree(root)`: Draws a branching ASCII hierarchy showing questions (`[?]`) and guesses (`[★]`) with `├──` and `└──` connectors.
- `MindReaderEngine`: A clean interactive REPL with menu options:
  1. Play 20-Questions (walks down the tree, guesses, and prompts for learning if incorrect).
  2. Display Visual Tree (ASCII terminal map).
  3. View Tree Analytics (Height, Leaves, Total Nodes).
  4. View Traversals.
  5. Reset to default seed.
  6. Exit.

---

## 🧪 Self-Verification Test Suite

Run this command at any time during your implementation:

```bash
python pydtree.py --test
```

All 7 test milestones must pass with output:

```text
============================================================
🧪 Running PyDTree Milestone Verification Test Suite...
============================================================
  ✓ Test 1: Node & Leaf properties verified.
  ✓ Test 2: Boundary edge cases (None, single node) verified.
  ✓ Test 3: Metrics on multi-level tree verified.
  ✓ Test 4: Pre-order, In-order, Post-order walks verified.
  ✓ Test 5: Dynamic Pointer Mutation (Knowledge Grafting) verified.
  ✓ Test 6: JSON Dictionary serialization round-trip verified.
  ✓ Test 7: Default seed knowledge tree verified.

============================================================
🎉 ALL 7 ASSIGNMENT UNIT TESTS PASSED! SCORE: 100/100
============================================================
```

---

## 🎨 Creative Challenge (Personal Verification)

To prove you built this with your own mind, add your own custom seed file or teach your tree at least **5 new concepts** (animals, programming languages, or sci-fi characters).

Then in your pull request description, paste:

1. The ASCII tree printout of your tree after it has learned 5 new concepts.
2. A short, 3-sentence explanation of: **"Why did we use Post-order traversal rather than Pre-order traversal if we wanted to calculate the total disk space of a folder hierarchy?"**
