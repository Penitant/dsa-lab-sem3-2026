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


class TreeNode:
    """A node in the decision tree.

    Leaf nodes contain a final guess. Internal nodes contain a Yes/No
    question and point to the corresponding subtrees.
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
        return self.yes_child is None and self.no_child is None

    def __repr__(self) -> str:
        if self.is_leaf():
            return f"Leaf('{self.text}')"
        return f"Decision('{self.text}')"


# =====================================================================
# Milestone 2: Tree Metrics & Structural Algorithms
# =====================================================================

def count_nodes(root: Optional[TreeNode]) -> int:
    """Return the total number of nodes in the tree."""
    if root is None:
        return 0
    return 1 + count_nodes(root.yes_child) + count_nodes(root.no_child)


def count_leaves(root: Optional[TreeNode]) -> int:
    """Return the number of leaf nodes (final guesses)."""
    if root is None:
        return 0
    if root.is_leaf():
        return 1
    return count_leaves(root.yes_child) + count_leaves(root.no_child)


def tree_height(root: Optional[TreeNode]) -> int:
    """Return tree height measured in edges (empty tree is -1)."""
    if root is None:
        return -1
    if root.is_leaf():
        return 0
    return 1 + max(
        tree_height(root.yes_child),
        tree_height(root.no_child),
    )


# =====================================================================
# Milestone 3: Tree Traversals
# =====================================================================

def preorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Visit Root -> Yes subtree -> No subtree."""
    if root is None:
        return []
    return (
        [root.text]
        + preorder_traversal(root.yes_child)
        + preorder_traversal(root.no_child)
    )


def postorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Visit Yes subtree -> No subtree -> Root."""
    if root is None:
        return []
    return (
        postorder_traversal(root.yes_child)
        + postorder_traversal(root.no_child)
        + [root.text]
    )


def inorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Visit Yes subtree -> Root -> No subtree."""
    if root is None:
        return []
    return (
        inorder_traversal(root.yes_child)
        + [root.text]
        + inorder_traversal(root.no_child)
    )


# =====================================================================
# Milestone 6: Terminal ASCII Tree Visualizer
# =====================================================================

def _print_subtree(
    node: TreeNode, choice: str, prefix: str, is_tail: bool
) -> None:
    branch = "└── " if is_tail else "├── "
    kind = "★ Guess" if node.is_leaf() else "? Question"
    print(prefix + branch + f"({choice}) [{kind}]: \"{node.text}\"")

    children = []
    if node.yes_child is not None:
        children.append(("Yes", node.yes_child))
    if node.no_child is not None:
        children.append(("No", node.no_child))

    for i, (child_choice, child) in enumerate(children):
        child_is_tail = i == len(children) - 1
        extension = "    " if is_tail else "│   "
        _print_subtree(
            child,
            child_choice,
            prefix + extension,
            child_is_tail,
        )


def print_ascii_tree(
    root: Optional[TreeNode], prefix: str = "", is_tail: bool = True
) -> None:
    """Print a branching ASCII representation of the tree."""
    if root is None:
        print("(empty tree)")
        return

    branch = "└── " if is_tail else "├── "
    kind = "★ Guess" if root.is_leaf() else "? Question"
    print(prefix + branch + f"[{kind}]: \"{root.text}\"")

    children = []
    if root.yes_child is not None:
        children.append(("Yes", root.yes_child))
    if root.no_child is not None:
        children.append(("No", root.no_child))

    for i, (choice, child) in enumerate(children):
        child_is_tail = i == len(children) - 1
        extension = "    " if is_tail else "│   "
        _print_subtree(child, choice, prefix + extension, child_is_tail)


# =====================================================================
# Milestone 4: Knowledge Tree Serialization (Save / Load)
# =====================================================================

def tree_to_dict(root: Optional[TreeNode]) -> Optional[Dict[str, Any]]:
    """Convert a TreeNode hierarchy into a JSON-serializable dictionary."""
    if root is None:
        return None

    if root.is_leaf():
        return {"guess": root.text}

    return {
        "question": root.text,
        "yes": tree_to_dict(root.yes_child),
        "no": tree_to_dict(root.no_child),
    }


def dict_to_tree(data: Optional[Dict[str, Any]]) -> Optional[TreeNode]:
    """Reconstruct a TreeNode hierarchy from its nested dictionary."""
    if data is None:
        return None

    if "guess" in data:
        return TreeNode(data["guess"])

    if "question" in data:
        return TreeNode(
            data["question"],
            dict_to_tree(data.get("yes")),
            dict_to_tree(data.get("no")),
        )

    raise ValueError("Invalid tree dictionary: expected 'guess' or 'question'.")


def save_tree_to_file(root: TreeNode, filename: str) -> None:
    """Save the tree structure to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tree_to_dict(root), file, indent=2)


def load_tree_from_file(filename: str) -> TreeNode:
    """Load a tree from a JSON file."""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

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
    """Turn an existing guess leaf into a question with two new guess leaves."""
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


def create_default_seed_tree() -> TreeNode:
    """Return a small starter tree containing three animal guesses."""
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
    """Interactive 20-Questions game powered by the decision tree."""

    def __init__(self, seed_file: Optional[str] = None):
        self.knowledge_file = seed_file or "dtree_knowledge.json"
        try:
            self.root = load_tree_from_file(self.knowledge_file)
            print(
                f"[*] Loaded existing knowledge base from "
                f"'{self.knowledge_file}'."
            )
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self.root = create_default_seed_tree()
            print("[*] Initialized fresh default knowledge seed tree.")

    def ask_yes_no(self, prompt: str) -> bool:
        """Read and validate a Yes/No response."""
        while True:
            answer = input(f"{prompt} (yes/no): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please enter 'yes' or 'no'.")

    def play_round(self) -> None:
        """Play one round and teach the tree if its guess is incorrect."""
        print("\n" + "─" * 50)
        print("🤔 Think of any animal, character, or everyday object.")
        print("I will try to guess it by asking Yes/No questions!")
        print("─" * 50)
        input("Press [Enter] when you are ready...")

        current = self.root
        while not current.is_leaf():
            answer = self.ask_yes_no(current.text)
            current = current.yes_child if answer else current.no_child

        print(f"\n🔮 My guess is: Is it a {current.text}?")
        won = self.ask_yes_no("Did I get it right?")

        if won:
            print("\n🎉 Aha! Never underestimate binary decision trees!")
            return

        print("\n😔 My current knowledge base needs to learn.")
        new_item = input("What were you actually thinking of? > ").strip()
        if not new_item:
            print("No answer provided. Skipping learning step.")
            return

        old_guess = current.text
        question = input(
            f"Give me a Yes/No question that distinguishes "
            f"'{new_item}' from '{old_guess}':\n> "
        ).strip()
        if not question.endswith("?"):
            question += "?"

        answer_for_new = self.ask_yes_no(
            f"For '{new_item}', what is the correct answer?"
        )

        graft_new_knowledge(
            current, question, new_item, answer_for_new
        )
        print(f"\n✨ Brain updated! I have learned '{new_item}'.")

        try:
            save_tree_to_file(self.root, self.knowledge_file)
            print(
                f"[✓] Updated tree saved to '{self.knowledge_file}'."
            )
        except Exception as error:
            print(f"[!] Warning: Could not save knowledge file: {error}")

    def start_repl(self) -> None:
        """Run the interactive menu."""
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
                print("\n🌳 Current Knowledge Tree:")
                print_ascii_tree(self.root)
            elif choice == "3":
                print("\n📊 Tree Structural Analytics:")
                print(f"  • Total Nodes:  {count_nodes(self.root)}")
                print(f"  • Total Leaves: {count_leaves(self.root)}")
                print(f"  • Tree Height:  {tree_height(self.root)} edges")
            elif choice == "4":
                print("\n🚶 Tree Traversals:")
                print(f"  • Pre-order:  {preorder_traversal(self.root)}")
                print(f"  • In-order:   {inorder_traversal(self.root)}")
                print(f"  • Post-order: {postorder_traversal(self.root)}")
            elif choice == "5":
                if self.ask_yes_no(
                    "Are you sure you want to reset the knowledge?"
                ):
                    self.root = create_default_seed_tree()
                    save_tree_to_file(self.root, self.knowledge_file)
                    print("[✓] Knowledge base reset.")
            elif choice == "6" or choice.lower() in ("exit", "quit", "q"):
                print("Goodbye! Keep exploring non-linear data structures.")
                break
            else:
                print("Invalid selection. Choose a number between 1 and 6.")


# =====================================================================
# Milestone 7: Automated Unit Test Suite
# =====================================================================

def run_tests() -> None:
    """Validate the assignment milestones."""
    print("=" * 60)
    print("🧪 Running PyDTree Milestone Verification Test Suite...")
    print("=" * 60)

    # Test 1: Node creation and leaf property
    leaf = TreeNode("Cheetah")
    assert leaf.is_leaf() is True, "A leaf should have no children."
    internal = TreeNode(
        "Has stripes?", yes_child=leaf, no_child=TreeNode("Lion")
    )
    assert internal.is_leaf() is False
    print("  ✓ Test 1: Node & Leaf properties verified.")

    # Test 2: Empty and single-node trees
    assert count_nodes(None) == 0
    assert count_leaves(None) == 0
    assert tree_height(None) == -1
    assert tree_height(leaf) == 0
    assert count_leaves(leaf) == 1
    print("  ✓ Test 2: Boundary edge cases (None, single node) verified.")

    # Test 3: Metrics on a small tree
    assert count_nodes(internal) == 3
    assert count_leaves(internal) == 2
    assert tree_height(internal) == 1
    print("  ✓ Test 3: Metrics on multi-level tree verified.")

    # Test 4: Traversals
    assert preorder_traversal(internal) == [
        "Has stripes?", "Cheetah", "Lion"
    ]
    assert postorder_traversal(internal) == [
        "Cheetah", "Lion", "Has stripes?"
    ]
    assert inorder_traversal(internal) == [
        "Cheetah", "Has stripes?", "Lion"
    ]
    print("  ✓ Test 4: Pre-order, In-order, Post-order walks verified.")

    # Test 5: Dynamic knowledge grafting
    lion_leaf = internal.no_child
    graft_new_knowledge(
        lion_leaf,
        "Does it have a mane?",
        "Lioness",
        new_guess_is_yes=False,
    )
    assert not lion_leaf.is_leaf()
    assert lion_leaf.text == "Does it have a mane?"
    assert lion_leaf.yes_child.text == "Lion"
    assert lion_leaf.no_child.text == "Lioness"
    assert tree_height(internal) == 2
    assert count_leaves(internal) == 3
    print("  ✓ Test 5: Dynamic Pointer Mutation (Knowledge Grafting) verified.")

    # Test 6: Serialization and deserialization
    tree_dict = tree_to_dict(internal)
    reconstructed = dict_to_tree(tree_dict)
    assert count_nodes(reconstructed) == count_nodes(internal)
    assert preorder_traversal(reconstructed) == preorder_traversal(internal)
    print("  ✓ Test 6: JSON Dictionary serialization round-trip verified.")

    # Test 7: Default seed tree
    seed = create_default_seed_tree()
    assert count_nodes(seed) == 5
    assert count_leaves(seed) == 3
    assert tree_height(seed) == 2
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
