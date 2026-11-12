"""
PyDTree - The Adaptive Knowledge Tree & 20-Questions Engine
Lab 4 Assignment: Non-Linear Hierarchies & Self-Learning Decision Trees
"""

import sys
import json
from typing import Optional, Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# =====================================================================
# Milestone 1: The Decision Tree Node
# =====================================================================


class TreeNode:
    """A node in the Decision Tree (leaf = guess, internal = question)."""

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
# Milestone 2: Tree Metrics
# =====================================================================


def count_nodes(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    return 1 + count_nodes(root.yes_child) + count_nodes(root.no_child)


def count_leaves(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0
    if root.is_leaf():
        return 1
    return count_leaves(root.yes_child) + count_leaves(root.no_child)


def tree_height(root: Optional[TreeNode]) -> int:
    if root is None:
        return -1
    if root.is_leaf():
        return 0
    return 1 + max(tree_height(root.yes_child), tree_height(root.no_child))


# =====================================================================
# Milestone 3: Tree Traversals
# =====================================================================


def preorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Root -> Yes (Left) -> No (Right)."""
    if root is None:
        return []
    return (
        [root.text]
        + preorder_traversal(root.yes_child)
        + preorder_traversal(root.no_child)
    )


def inorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Yes (Left) -> Root -> No (Right)."""
    if root is None:
        return []
    return (
        inorder_traversal(root.yes_child)
        + [root.text]
        + inorder_traversal(root.no_child)
    )


def postorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Yes (Left) -> No (Right) -> Root."""
    if root is None:
        return []
    return (
        postorder_traversal(root.yes_child)
        + postorder_traversal(root.no_child)
        + [root.text]
    )


# =====================================================================
# Milestone 4: Serialization (Save / Load)
# =====================================================================


def tree_to_dict(root: Optional[TreeNode]) -> Optional[Dict[str, Any]]:
    """Recursively converts a TreeNode hierarchy into a JSON-serializable dict."""
    if root is None:
        return None
    if root.is_leaf():
        return {"guess": root.text}
    if root.yes_child is None or root.no_child is None:
        return None
    return {
        "question": root.text,
        "yes": tree_to_dict(root.yes_child),
        "no": tree_to_dict(root.no_child),
    }


def dict_to_tree(data: Optional[Dict[str, Any]]) -> Optional[TreeNode]:
    """Recursively reconstructs a TreeNode hierarchy from a dictionary."""
    if not isinstance(data, dict):
        return None

    if "guess" in data:
        if len(data) != 1:
            return None
        if not isinstance(data["guess"], str) or not data["guess"].strip():
            return None
        return TreeNode(data["guess"])

    if "question" in data:
        if len(data) != 3 or "yes" not in data or "no" not in data:
            return None
        if not isinstance(data["question"], str) or not data["question"].strip():
            return None

        yes_child = dict_to_tree(data["yes"])
        no_child = dict_to_tree(data["no"])
        if yes_child is None or no_child is None:
            return None
        return TreeNode(data["question"], yes_child, no_child)

    return None


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
        raise ValueError("File contains an empty or invalid tree structure.")
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
    """Mutates an existing leaf node into a new question node in-place."""
    old_guess = leaf_node.text

    new_guess_node = TreeNode(new_guess)
    old_guess_node = TreeNode(old_guess)

    leaf_node.text = new_question.strip()

    if new_guess_is_yes:
        leaf_node.yes_child = new_guess_node
        leaf_node.no_child = old_guess_node
    else:
        leaf_node.yes_child = old_guess_node
        leaf_node.no_child = new_guess_node


# =====================================================================
# Default seed (cricketers)
# =====================================================================


def default_seed():
    return {
        "question": "Is he known as Captain Cool?",
        "yes": {
            "guess": "MS Dhoni"
        },
        "no": {
            "question": "Is the cricketer primarily known as a batsman?",
            "yes": {
                "question": "Is he known as the King of Cricket?",
                "yes": {
                    "guess": "Virat Kohli"
                },
                "no": {
                    "question": "Is he known as the Hitman?",
                    "yes": {
                        "guess": "Rohit Sharma"
                    },
                    "no": {
                        "guess": "Sachin Tendulkar"
                    }
                }
            },
            "no": {
                "question": "Is he a fast bowler?",
                "yes": {
                    "guess": "Jasprit Bumrah"
                },
                "no": {
                    "guess": "Ravichandran Ashwin"
                }
            }
        }
    }


def create_default_seed_tree() -> TreeNode:
    """Returns the default cricketer seed tree."""
    return dict_to_tree(default_seed())


# =====================================================================
# Milestone 6: Terminal ASCII Tree Visualizer
# =====================================================================


def print_ascii_tree(
    root: Optional[TreeNode], prefix: str = "", is_tail: bool = True
) -> None:
    """Prints a branching ASCII diagram: [?] questions, [★] guesses."""
    if root is None:
        print("(empty tree)")
        return

    def display(node: TreeNode, prefix: str, is_tail: bool, label: str, is_root: bool):
        marker = "[★] " if node.is_leaf() else "[?] "
        text = (f"({label}) " if label else "") + marker + node.text

        if is_root:
            print(text)
            child_prefix = ""
        else:
            print(prefix + ("└── " if is_tail else "├── ") + text)
            child_prefix = prefix + ("    " if is_tail else "│   ")

        children = []
        if node.yes_child is not None:
            children.append(("Yes", node.yes_child))
        if node.no_child is not None:
            children.append(("No", node.no_child))

        for i, (child_label, child) in enumerate(children):
            display(child, child_prefix, i == len(children) - 1, child_label, False)

    display(root, prefix, is_tail, "", True)


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
        """Validated Yes/No input; keeps asking until the answer is valid."""
        while True:
            ans = input(f"{prompt} (yes/no): ").strip().lower()
            if ans in ("y", "yes"):
                return True
            if ans in ("n", "no"):
                return False
            print("Please enter 'yes' or 'no'.")

    def play_round(self) -> None:
        print("\n" + "─" * 50)
        print("🤔 Think of a cricketer (or anything else you like).")
        print("I will try to guess it by asking Yes/No questions!")
        print("─" * 50)
        input("Press [Enter] when you are ready...")

        curr = self.root
        while not curr.is_leaf():
            curr = curr.yes_child if self.ask_yes_no(curr.text) else curr.no_child

        print(f"\n🔮 My guess is: Is it {curr.text}?")
        if self.ask_yes_no("Did I get it right?"):
            print("\n🎉 Aha! Never underestimate the power of binary decision trees!")
            return

        print("\n😔 Drat! You outsmarted my current knowledge base.")
        new_item = input("What were you actually thinking of? > ").strip()
        if not new_item:
            print("No answer provided. Skipping learning step.")
            return

        old_guess = curr.text
        dist_question = input(
            f"Give me a Yes/No question that distinguishes '{new_item}' from '{old_guess}':\n> "
        ).strip()
        if not dist_question:
            print("No question provided. Skipping learning step.")
            return
        if not dist_question.endswith("?"):
            dist_question += "?"

        ans_for_new = self.ask_yes_no(f"For '{new_item}', what is the correct answer?")

        graft_new_knowledge(curr, dist_question, new_item, ans_for_new)
        print(f"\n✨ Brain updated! I have spliced '{new_item}' into my hierarchy.")

        try:
            save_tree_to_file(self.root, self.knowledge_file)
            print(f"[✓] Persisted updated tree to '{self.knowledge_file}'.")
        except Exception as e:
            print(f"[!] Warning: Could not save knowledge file: {e}")

    def start_repl(self) -> None:
        print("=" * 60)
        print("  🌲 MindReader 2000 — Adaptive Knowledge Tree Engine")
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
    print("=" * 60)
    print("🧪 Running PyDTree Milestone Verification Test Suite...")
    print("=" * 60)

    # Test 1
    n_leaf = TreeNode("Cheetah")
    assert n_leaf.is_leaf() is True, "Test 1 Failed: Leaf node should be a leaf"
    n_internal = TreeNode("Has stripes?", yes_child=n_leaf, no_child=TreeNode("Lion"))
    assert n_internal.is_leaf() is False, "Test 1 Failed: Internal node is not a leaf"
    print("  ✓ Test 1: Node & Leaf properties verified.")

    # Test 2
    assert count_nodes(None) == 0, "Test 2 Failed: Empty tree count should be 0"
    assert count_leaves(None) == 0, "Test 2 Failed: Empty tree leaves should be 0"
    assert tree_height(None) == -1, "Test 2 Failed: Empty tree height should be -1"
    assert tree_height(n_leaf) == 0, "Test 2 Failed: Single node height should be 0"
    assert count_leaves(n_leaf) == 1, "Test 2 Failed: Single node leaf count is 1"
    print("  ✓ Test 2: Boundary edge cases (None, single node) verified.")

    # Test 3
    assert count_nodes(n_internal) == 3, "Test 3 Failed: Total node count should be 3"
    assert count_leaves(n_internal) == 2, "Test 3 Failed: Total leaves should be 2"
    assert tree_height(n_internal) == 1, "Test 3 Failed: Tree height should be 1"
    print("  ✓ Test 3: Metrics on multi-level tree verified.")

    # Test 4
    pre = preorder_traversal(n_internal)
    assert pre == ["Has stripes?", "Cheetah", "Lion"], f"Test 4 Failed: Pre-order: {pre}"
    post = postorder_traversal(n_internal)
    assert post == ["Cheetah", "Lion", "Has stripes?"], f"Test 4 Failed: Post-order: {post}"
    ino = inorder_traversal(n_internal)
    assert ino == ["Cheetah", "Has stripes?", "Lion"], f"Test 4 Failed: In-order: {ino}"
    print("  ✓ Test 4: Pre-order, In-order, Post-order walks verified.")

    # Test 5
    lion_leaf = n_internal.no_child
    graft_new_knowledge(
        lion_leaf, "Does it have a mane?", "Lioness", new_guess_is_yes=False
    )
    assert not lion_leaf.is_leaf(), "Test 5 Failed: Grafted node should be internal"
    assert lion_leaf.text == "Does it have a mane?"
    assert lion_leaf.yes_child.text == "Lion"
    assert lion_leaf.no_child.text == "Lioness"
    assert tree_height(n_internal) == 2, "Test 5 Failed: Height should be 2"
    assert count_leaves(n_internal) == 3, "Test 5 Failed: Leaves should be 3"
    print("  ✓ Test 5: Dynamic Pointer Mutation (Knowledge Grafting) verified.")

    # Test 6
    tree_dict = tree_to_dict(n_internal)
    reconstructed = dict_to_tree(tree_dict)
    assert count_nodes(reconstructed) == count_nodes(n_internal), "Test 6 Failed: count"
    assert preorder_traversal(reconstructed) == preorder_traversal(n_internal), (
        "Test 6 Failed: walk mismatch"
    )
    assert tree_to_dict(reconstructed) == tree_dict, "Test 6 Failed: dict mismatch"
    print("  ✓ Test 6: JSON Dictionary serialization round-trip verified.")

    # Test 7: cricketer seed -> 11 nodes, 6 leaves, height 4
    seed = create_default_seed_tree()
    assert seed is not None, "Test 7 Failed: Seed tree could not be built"
    assert count_nodes(seed) == 11, f"Test 7 Failed: nodes = {count_nodes(seed)}"
    assert count_leaves(seed) == 6, f"Test 7 Failed: leaves = {count_leaves(seed)}"
    assert tree_height(seed) == 4, f"Test 7 Failed: height = {tree_height(seed)}"
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