"""
PyDTree - The Adaptive Knowledge Tree & 20-Questions Engine
Lab 4 Assignment: Non-Linear Hierarchies & Self-Learning Decision Trees

A hands-on project to master Trees, Recursion, Dynamic Pointer Grafting,
Tree Traversals, and Hierarchical Data Representation.
"""

import sys
import json
from typing import Optional, Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


class TreeNode:
    """A node in the Decision Tree.

    If it is a leaf:
      `text` is the final guess/answer (e.g. 'Dog', 'Smartphone').
      `yes_child` and `no_child` are both None.

    If it is an internal decision node:
      `text` is a distinguishing Yes/No question (e.g. 'Does it have fur?').
      `yes_child` points to the subtree if the answer is Yes.
      `no_child` points to the subtree if the answer is No.
    """

    def __init__(
        self,
        text: str,
        yes_child: Optional["TreeNode"] = None,
        no_child: Optional["TreeNode"] = None,
    ):
        self.text: str = text.strip()
        self.yes_child: Optional["TreeNode"] = yes_child
        self.no_child: Optional["TreeNode"] = no_child

    def is_leaf(self) -> bool:
        """Returns True if this node has no children (i.e. it is a guess)."""
        return self.yes_child is None and self.no_child is None

    def __repr__(self) -> str:
        if self.is_leaf():
            return f"Leaf('{self.text}')"
        return f"Decision('{self.text}')"


# =====================================================================
# Milestone 2: Tree Metrics & Structural Algorithms
# =====================================================================


def count_nodes(root: Optional[TreeNode]) -> int:
    """Returns the total number of nodes in the tree.

    Base case: Empty tree has 0 nodes.
    Recursive step: 1 + count(left) + count(right)
    """
    # TODO: implement this function
    raise NotImplementedError


def count_leaves(root: Optional[TreeNode]) -> int:
    """Returns the number of leaf nodes (final guesses)."""
    # TODO: implement this function
    raise NotImplementedError


def tree_height(root: Optional[TreeNode]) -> int:
    """Returns the height of the tree.

    By standard convention:
      - Empty tree height: -1
      - Single node tree height: 0
      - Otherwise: 1 + max(height(left), height(right))
    """
    # TODO: implement this function
    raise NotImplementedError


# =====================================================================
# Milestone 3: Tree Traversals
# =====================================================================


def preorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Root -> Yes (Left) -> No (Right).
    Used to serialize and inspect the hierarchical tree from the top down.
    """
    # TODO: implement this function
    raise NotImplementedError


def postorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Yes (Left) -> No (Right) -> Root.
    Used for bottom-up operations (e.g. calculating subtree memory, pruning).
    """
    # TODO: implement this function
    raise NotImplementedError


def inorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Yes (Left) -> Root -> No (Right)."""
    # TODO: implement this function
    raise NotImplementedError


# =====================================================================
# Milestone 6: Terminal ASCII Tree Visualizer
# =====================================================================


def print_ascii_tree(
    root: Optional[TreeNode], prefix: str = "", is_tail: bool = True
) -> None:
    """Prints a beautiful visual branching diagram of the tree in the terminal."""
    if root is None:
        print("(empty tree)")
        return

    node_label = f"[{'★ Guess' if root.is_leaf() else '? Question'}]: \"{root.text}\""
    branch = "└── " if is_tail else "├── "
    print(prefix + branch + node_label)

    children = []
    if root.yes_child:
        children.append(("Yes", root.yes_child))
    if root.no_child:
        children.append(("No", root.no_child))

    for i, (choice, child) in enumerate(children):
        child_is_tail = i == len(children) - 1
        extension = "    " if is_tail else "│   "
        child_prefix = prefix + extension
        branch_label = f"({choice}) "
        # Print child with branch label
        sub_branch = "└── " if child_is_tail else "├── "
        child_node_label = f"{branch_label}[{'★ Guess' if child.is_leaf() else '? Question'}]: \"{child.text}\""
        print(child_prefix + sub_branch + child_node_label)

        # Now print grandchild branches if any
        grand_children = []
        if child.yes_child:
            grand_children.append(("Yes", child.yes_child))
        if child.no_child:
            grand_children.append(("No", child.no_child))

        for gi, (g_choice, g_child) in enumerate(grand_children):
            g_is_tail = gi == len(grand_children) - 1
            g_ext = "    " if child_is_tail else "│   "
            _print_subtree(g_child, g_choice, child_prefix + g_ext, g_is_tail)


def _print_subtree(node: TreeNode, choice: str, prefix: str, is_tail: bool) -> None:
    branch = "└── " if is_tail else "├── "
    label = (
        f"({choice}) [{'★ Guess' if node.is_leaf() else '? Question'}]: \"{node.text}\""
    )
    print(prefix + branch + label)

    children = []
    if node.yes_child:
        children.append(("Yes", node.yes_child))
    if node.no_child:
        children.append(("No", node.no_child))

    for i, (c_choice, child) in enumerate(children):
        c_tail = i == len(children) - 1
        ext = "    " if is_tail else "│   "
        _print_subtree(child, c_choice, prefix + ext, c_tail)


# =====================================================================
# Milestone 4: Knowledge Tree Serialization (Save / Load)
# =====================================================================


def tree_to_dict(root: Optional[TreeNode]) -> Optional[Dict[str, Any]]:
    """Recursively converts a TreeNode hierarchy into a JSON-serializable dictionary."""
    # TODO: implement this function
    raise NotImplementedError


def dict_to_tree(data: Optional[Dict[str, Any]]) -> Optional[TreeNode]:
    """Recursively reconstructs a TreeNode hierarchy from a dictionary."""
    # TODO: implement this function
    raise NotImplementedError


def save_tree_to_file(root: TreeNode, filename: str) -> None:
    """Saves the tree structure to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tree_to_dict(root), f, indent=2)


def load_tree_from_file(filename: str) -> TreeNode:
    """Loads a tree from a JSON file, or raises FileNotFoundError."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    tree = dict_to_tree(data)
    if tree is None:
        raise ValueError("File contains an empty tree structure.")
    return tree


# =====================================================================
# Milestone 5: Dynamic Pointer Mutation (Grafting New Knowledge)
# =====================================================================


def graft_new_knowledge(
    leaf_node: TreeNode,
    new_question: str,
    new_guess: str,
    new_guess_is_yes: bool,
) -> None:
    """Mutates an existing leaf node into a new question node in-place.

    This is the heart of the adaptive decision tree:
    The old leaf's guess is preserved as one branch, and the new guess
    becomes the other branch. The current node's text becomes the distinguishing question.

    Example:
      Old leaf: 'Dog'
      User was thinking of: 'Cat'
      Distinguishing question: 'Does it meow?'
      For Cat, answer is: Yes

      Transformation:
        Node becomes: Question('Does it meow?')
        yes_child becomes: Leaf('Cat')
        no_child becomes: Leaf('Dog')
    """
    # TODO: implement this function
    raise NotImplementedError


def create_default_seed_tree() -> TreeNode:
    """Returns a beginner seed tree with a few animals to start learning immediately."""
    root = TreeNode("Does it live in water?")
    root.yes_child = TreeNode("Dolphin")

    land_branch = TreeNode("Does it bark?")
    land_branch.yes_child = TreeNode("Dog")
    land_branch.no_child = TreeNode("Elephant")

    root.no_child = land_branch
    return root


# =====================================================================
# Milestone 6: Interactive Terminal Game Engine
# =====================================================================


class MindReaderEngine:
    """The interactive 20-Questions Engine powered by your Decision Tree."""

    def __init__(self, seed_file: Optional[str] = None):
        self.knowledge_file = seed_file or "dtree_knowledge.json"
        try:
            self.root = load_tree_from_file(self.knowledge_file)
            print(f"[*] Loaded existing knowledge base from '{self.knowledge_file}'.")
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self.root = create_default_seed_tree()
            print("[*] Initialized fresh default knowledge seed tree.")

    def ask_yes_no(self, prompt: str) -> bool:
        """Helper to get a validated Yes/No response from the terminal user."""
        while True:
            ans = input(f"{prompt} (yes/no): ").strip().lower()
            if ans in ("y", "yes"):
                return True
            if ans in ("n", "no"):
                return False
            print("Please enter 'yes' or 'no'.")

    def play_round(self) -> None:
        """Plays one full game of 20-Questions, walking down the tree and learning if wrong."""
        print("\n" + "─" * 50)
        print("🤔 Think of any animal, character, or everyday object.")
        print("I will try to guess it by asking Yes/No questions!")
        print("─" * 50)
        input("Press [Enter] when you are ready...")

        curr = self.root
        while not curr.is_leaf():
            ans = self.ask_yes_no(curr.text)
            curr = curr.yes_child if ans else curr.no_child

        # We arrived at a leaf node guess!
        print(f"\n🔮 My guess is: Is it a {curr.text}?")
        won = self.ask_yes_no("Did I get it right?")

        if won:
            print("\n🎉 Aha! Never underestimate the power of binary decision trees!")
            return

        # The computer was wrong -> Teach the tree!
        print("\n😔 Drat! You outsmarted my current knowledge base.")
        new_item = input("What were you actually thinking of? > ").strip()
        if not new_item:
            print("No answer provided. Skipping learning step.")
            return

        old_guess = curr.text
        dist_question = input(
            f"Give me a Yes/No question that distinguishes a '{new_item}' from a '{old_guess}':\n> "
        ).strip()
        if not dist_question.endswith("?"):
            dist_question += "?"

        ans_for_new = self.ask_yes_no(
            f"For a '{new_item}', what is the correct answer?"
        )

        # Mutate the leaf pointer
        graft_new_knowledge(curr, dist_question, new_item, ans_for_new)
        print(f"\n✨ Brain updated! I have spliced '{new_item}' into my hierarchy.")

        # Save to disk
        try:
            save_tree_to_file(self.root, self.knowledge_file)
            print(f"[✓] Persisted updated tree to '{self.knowledge_file}'.")
        except Exception as e:
            print(f"[!] Warning: Could not save knowledge file: {e}")

    def start_repl(self) -> None:
        """Terminal interactive loop for playing, viewing, and testing."""
        print("=" * 60)
        print("  🌲 MindReader 2000 — Adaptive Knowledge Tree Engine")
        print("  ECS25 Lab 4: Tree Hierarchies & Dynamic Pointer Grafting")
        print("=" * 60)

        while True:
            print("\n[Menu Options]:")
            print("  1. Play 20-Questions (Teach the tree)")
            print("  2. Display Visual Tree (ASCII terminal map)")
            print("  3. View Tree Statistics (Height, Leaves, Nodes)")
            print("  4. View Traversals (Pre-order, In-order, Post-order)")
            print("  5. Reset to Default Seed Tree")
            print("  6. Exit")

            choice = input("\nEnter choice [1-6]: ").strip()
            if choice == "1":
                self.play_round()
            elif choice == "2":
                print("\n🌳 Current Knowledge Tree Topology:")
                print_ascii_tree(self.root)
            elif choice == "3":
                print("\n📊 Tree Structural Analytics:")
                print(f"  • Total Nodes:  {count_nodes(self.root)}")
                print(f"  • Total Leaves: {count_leaves(self.root)} (Known Concepts)")
                print(f"  • Tree Height:  {tree_height(self.root)} edges")
            elif choice == "4":
                print("\n🚶 Tree Walks:")
                print(f"  • Pre-order:  {preorder_traversal(self.root)}")
                print(f"  • In-order:   {inorder_traversal(self.root)}")
                print(f"  • Post-order: {postorder_traversal(self.root)}")
            elif choice == "5":
                if self.ask_yes_no(
                    "Are you sure you want to reset knowledge to default?"
                ):
                    self.root = create_default_seed_tree()
                    save_tree_to_file(self.root, self.knowledge_file)
                    print("[✓] Knowledge base reset.")
            elif choice == "6" or choice.lower() in ("exit", "quit", "q"):
                print("Goodbye! Keep exploring non-linear data structures.")
                break
            else:
                print("Invalid selection. Please choose a number between 1 and 6.")


# =====================================================================
# Milestone 7: Automated Unit Test Suite
# =====================================================================


def run_tests() -> None:
    """Validates all milestones for automated assignment grading."""
    print("=" * 60)
    print("🧪 Running PyDTree Milestone Verification Test Suite...")
    print("=" * 60)

    # Test 1: Node creation & leaf property
    n_leaf = TreeNode("Cheetah")
    assert (
        n_leaf.is_leaf() is True
    ), "Test 1 Failed: Leaf node should have is_leaf() == True"
    n_internal = TreeNode("Has stripes?", yes_child=n_leaf, no_child=TreeNode("Lion"))
    assert (
        n_internal.is_leaf() is False
    ), "Test 1 Failed: Internal node should have is_leaf() == False"
    print("  ✓ Test 1: Node & Leaf properties verified.")

    # Test 2: Tree metrics on empty and single-node trees
    assert count_nodes(None) == 0, "Test 2 Failed: Empty tree count should be 0"
    assert count_leaves(None) == 0, "Test 2 Failed: Empty tree leaves should be 0"
    assert tree_height(None) == -1, "Test 2 Failed: Empty tree height should be -1"
    assert tree_height(n_leaf) == 0, "Test 2 Failed: Single node height should be 0"
    assert (
        count_leaves(n_leaf) == 1
    ), "Test 2 Failed: Single node leaf count should be 1"
    print("  ✓ Test 2: Boundary edge cases (None, single node) verified.")

    # Test 3: Metrics on small tree
    #      (Has stripes?)
    #       /          \
    #   (Cheetah)     (Lion)
    assert count_nodes(n_internal) == 3, "Test 3 Failed: Total node count should be 3"
    assert count_leaves(n_internal) == 2, "Test 3 Failed: Total leaves should be 2"
    assert tree_height(n_internal) == 1, "Test 3 Failed: Tree height should be 1"
    print("  ✓ Test 3: Metrics on multi-level tree verified.")

    # Test 4: Traversals
    pre = preorder_traversal(n_internal)
    assert pre == [
        "Has stripes?",
        "Cheetah",
        "Lion",
    ], f"Test 4 Failed: Pre-order incorrect: {pre}"
    post = postorder_traversal(n_internal)
    assert post == [
        "Cheetah",
        "Lion",
        "Has stripes?",
    ], f"Test 4 Failed: Post-order incorrect: {post}"
    ino = inorder_traversal(n_internal)
    assert ino == [
        "Cheetah",
        "Has stripes?",
        "Lion",
    ], f"Test 4 Failed: In-order incorrect: {ino}"
    print("  ✓ Test 4: Pre-order, In-order, Post-order walks verified.")

    # Test 5: Dynamic Knowledge Grafting (Pointer Mutation)
    # Graft onto Lion:
    # Lion is replaced by: "Does it have a mane?" -> Yes: Lion, No: Lioness
    lion_leaf = n_internal.no_child
    graft_new_knowledge(
        lion_leaf, "Does it have a mane?", "Lioness", new_guess_is_yes=False
    )
    assert (
        not lion_leaf.is_leaf()
    ), "Test 5 Failed: Grafted node should now be an internal node"
    assert lion_leaf.text == "Does it have a mane?"
    assert lion_leaf.yes_child.text == "Lion"
    assert lion_leaf.no_child.text == "Lioness"
    # Test height after graft
    assert (
        tree_height(n_internal) == 2
    ), "Test 5 Failed: Height should have increased to 2"
    assert count_leaves(n_internal) == 3, "Test 5 Failed: Leaves should now be 3"
    print("  ✓ Test 5: Dynamic Pointer Mutation (Knowledge Grafting) verified.")

    # Test 6: Serialization & Deserialization
    tree_dict = tree_to_dict(n_internal)
    reconstructed = dict_to_tree(tree_dict)
    assert count_nodes(reconstructed) == count_nodes(
        n_internal
    ), "Test 6 Failed: Reconstructed node count mismatch"
    assert preorder_traversal(reconstructed) == preorder_traversal(
        n_internal
    ), "Test 6 Failed: Reconstructed walk mismatch"
    print("  ✓ Test 6: JSON Dictionary serialization round-trip verified.")

    # Test 7: Default seed tree sanity check
    seed = create_default_seed_tree()
    assert (
        count_nodes(seed) == 5
    ), f"Test 7 Failed: Default seed tree should have 5 nodes, got {count_nodes(seed)}"
    assert (
        count_leaves(seed) == 3
    ), f"Test 7 Failed: Default seed tree should have 3 leaves, got {count_leaves(seed)}"
    assert (
        tree_height(seed) == 2
    ), f"Test 7 Failed: Default seed tree height should be 2, got {tree_height(seed)}"
    print("  ✓ Test 7: Default seed knowledge tree verified.")

    print("\n" + "=" * 60)
    print("🎉 ALL 7 ASSIGNMENT UNIT TESTS PASSED! SCORE: 100/100")
    print("Your Decision Tree engine is robust, correct, and ready to learn.")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        engine = MindReaderEngine()
        engine.start_repl()
