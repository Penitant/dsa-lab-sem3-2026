
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


# ============================================================
# Milestone 1: TreeNode Class
# ============================================================

class TreeNode:
    """A node in the Decision Tree."""

    def __init__(
        self,
        text: str,
        yes_child: Optional["TreeNode"] = None,
        no_child: Optional["TreeNode"] = None,
    ):
        self.text: str = text.strip()
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self) -> bool:
        """Returns True if the node has no children."""
        return self.yes_child is None and self.no_child is None

    def __repr__(self) -> str:
        if self.is_leaf():
            return f"Leaf('{self.text}')"
        return f"Decision('{self.text}')"


# ============================================================
# Milestone 2: Tree Metrics
# ============================================================

def count_nodes(root: Optional[TreeNode]) -> int:
    """Counts all nodes in the tree."""

    if root is None:
        return 0

    return (
        1
        + count_nodes(root.yes_child)
        + count_nodes(root.no_child)
    )


def count_leaves(root: Optional[TreeNode]) -> int:
    """Counts the leaf nodes in the tree."""

    if root is None:
        return 0

    if root.is_leaf():
        return 1

    return (
        count_leaves(root.yes_child)
        + count_leaves(root.no_child)
    )


def tree_height(root: Optional[TreeNode]) -> int:
    """Returns the height of the tree."""

    if root is None:
        return -1

    if root.is_leaf():
        return 0

    return 1 + max(
        tree_height(root.yes_child),
        tree_height(root.no_child)
    )


# ============================================================
# Milestone 3: Tree Traversals
# ============================================================

def preorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Root -> Yes -> No."""

    if root is None:
        return []

    result = [root.text]

    result += preorder_traversal(root.yes_child)
    result += preorder_traversal(root.no_child)

    return result


def postorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Yes -> No -> Root."""

    if root is None:
        return []

    result = []

    result += postorder_traversal(root.yes_child)
    result += postorder_traversal(root.no_child)

    result.append(root.text)

    return result


def inorder_traversal(root: Optional[TreeNode]) -> List[str]:
    """Yes -> Root -> No."""

    if root is None:
        return []

    result = []

    result += inorder_traversal(root.yes_child)
    result.append(root.text)
    result += inorder_traversal(root.no_child)

    return result


# ============================================================
# Milestone 4: ASCII Tree Visualizer
# ============================================================

def print_ascii_tree(
    root: Optional[TreeNode], prefix: str = "", is_tail: bool = True
) -> None:
    """Prints the tree structure in the terminal."""

    if root is None:
        print("(empty tree)")
        return

    node_label = (
        f"[{'★ Guess' if root.is_leaf() else '? Question'}]: "
        f"\"{root.text}\""
    )

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

        sub_branch = "└── " if child_is_tail else "├── "

        child_node_label = (
            f"({choice}) "
            f"[{'★ Guess' if child.is_leaf() else '? Question'}]: "
            f"\"{child.text}\""
        )

        print(child_prefix + sub_branch + child_node_label)

        grand_children = []

        if child.yes_child:
            grand_children.append(("Yes", child.yes_child))

        if child.no_child:
            grand_children.append(("No", child.no_child))

        for gi, (g_choice, g_child) in enumerate(grand_children):
            g_is_tail = gi == len(grand_children) - 1
            g_ext = "    " if child_is_tail else "│   "

            _print_subtree(
                g_child,
                g_choice,
                child_prefix + g_ext,
                g_is_tail
            )


def _print_subtree(
    node: TreeNode,
    choice: str,
    prefix: str,
    is_tail: bool
) -> None:

    branch = "└── " if is_tail else "├── "

    label = (
        f"({choice}) "
        f"[{'★ Guess' if node.is_leaf() else '? Question'}]: "
        f"\"{node.text}\""
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

        _print_subtree(
            child,
            c_choice,
            prefix + ext,
            c_tail
        )


# ============================================================
# Milestone 5: Tree Serialization (Save and Load)
# ============================================================

def tree_to_dict(
    root: Optional[TreeNode]
) -> Optional[Dict[str, Any]]:
    """Converts a tree into a dictionary."""

    if root is None:
        return None

    return {
        "text": root.text,
        "yes_child": tree_to_dict(root.yes_child),
        "no_child": tree_to_dict(root.no_child)
    }


def dict_to_tree(
    data: Optional[Dict[str, Any]]
) -> Optional[TreeNode]:
    """Converts a dictionary back into a tree."""

    if data is None:
        return None

    root = TreeNode(data["text"])

    root.yes_child = dict_to_tree(data.get("yes_child"))
    root.no_child = dict_to_tree(data.get("no_child"))

    return root


def save_tree_to_file(root: TreeNode, filename: str) -> None:
    """Saves the tree into a JSON file."""

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(tree_to_dict(root), f, indent=2)


def load_tree_from_file(filename: str) -> TreeNode:
    """Loads the tree from a JSON file."""

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    tree = dict_to_tree(data)

    if tree is None:
        raise ValueError("File contains an empty tree structure.")

    return tree


# ============================================================
# Milestone 6: Dynamic Pointer Mutation (Grafting)
# ============================================================

def graft_new_knowledge(
    leaf_node: TreeNode,
    new_question: str,
    new_guess: str,
    new_guess_is_yes: bool,
) -> None:
    """Changes an existing leaf into a question node."""

    old_guess = leaf_node.text

    old_node = TreeNode(old_guess)
    new_node = TreeNode(new_guess)

    leaf_node.text = new_question.strip()

    if not leaf_node.text.endswith("?"):
        leaf_node.text += "?"

    if new_guess_is_yes:
        leaf_node.yes_child = new_node
        leaf_node.no_child = old_node

    else:
        leaf_node.yes_child = old_node
        leaf_node.no_child = new_node


# ============================================================
# Default Seed Tree
# ============================================================

def create_default_seed_tree() -> TreeNode:
    """Creates the initial knowledge tree."""

    root = TreeNode("Does it live in water?")

    root.yes_child = TreeNode("Dolphin")

    land_branch = TreeNode("Does it bark?")
    land_branch.yes_child = TreeNode("Dog")
    land_branch.no_child = TreeNode("Elephant")

    root.no_child = land_branch

    return root


# ============================================================
# Milestone 7: Interactive Game Engine
# ============================================================

class MindReaderEngine:
    """The interactive 20-Questions engine."""

    def __init__(self, seed_file: Optional[str] = None):

        self.knowledge_file = seed_file or "dtree_knowledge.json"

        try:
            self.root = load_tree_from_file(self.knowledge_file)

            print(
                f"[*] Loaded existing knowledge base "
                f"from '{self.knowledge_file}'."
            )

        except (FileNotFoundError, json.JSONDecodeError, ValueError):

            self.root = create_default_seed_tree()

            print("[*] Initialized fresh default knowledge seed tree.")

    def ask_yes_no(self, prompt: str) -> bool:
        """Gets a valid Yes or No answer."""

        while True:

            ans = input(
                f"{prompt} (yes/no): "
            ).strip().lower()

            if ans in ("y", "yes"):
                return True

            if ans in ("n", "no"):
                return False

            print("Please enter 'yes' or 'no'.")

    def play_round(self) -> None:
        """Plays one round and learns new knowledge."""

        print("\n" + "─" * 50)

        print("🤔 Think of any animal, character, or everyday object.")
        print("I will try to guess it by asking Yes/No questions!")

        print("─" * 50)

        input("Press [Enter] when you are ready...")

        curr = self.root

        while not curr.is_leaf():

            ans = self.ask_yes_no(curr.text)

            if ans:
                curr = curr.yes_child
            else:
                curr = curr.no_child

        print(f"\n🔮 My guess is: Is it a {curr.text}?")

        won = self.ask_yes_no("Did I get it right?")

        if won:

            print(
                "\n🎉 Aha! Never underestimate "
                "the power of binary decision trees!"
            )

            return

        print("\n😔 Drat! You outsmarted my current knowledge base.")

        new_item = input(
            "What were you actually thinking of? > "
        ).strip()

        if not new_item:

            print("No answer provided. Skipping learning step.")
            return

        old_guess = curr.text

        dist_question = input(
            f"Give me a Yes/No question that distinguishes "
            f"a '{new_item}' from a '{old_guess}':\n> "
        ).strip()

        if not dist_question:
            print("No question provided. Skipping learning step.")
            return

        if not dist_question.endswith("?"):
            dist_question += "?"

        ans_for_new = self.ask_yes_no(
            f"For a '{new_item}', what is the correct answer?"
        )

        graft_new_knowledge(
            curr,
            dist_question,
            new_item,
            ans_for_new
        )

        print(
            f"\n✨ Brain updated! "
            f"I have spliced '{new_item}' into my hierarchy."
        )

        try:

            save_tree_to_file(
                self.root,
                self.knowledge_file
            )

            print(
                f"[✓] Persisted updated tree "
                f"to '{self.knowledge_file}'."
            )

        except Exception as e:

            print(f"[!] Warning: Could not save knowledge file: {e}")

    def start_repl(self) -> None:
        """Displays the interactive menu."""

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

                print(
                    f"  • Total Leaves: {count_leaves(self.root)} "
                    f"(Known Concepts)"
                )

                print(
                    f"  • Tree Height:  {tree_height(self.root)} edges"
                )

            elif choice == "4":

                print("\n🚶 Tree Walks:")

                print(
                    f"  • Pre-order:  {preorder_traversal(self.root)}"
                )

                print(
                    f"  • In-order:   {inorder_traversal(self.root)}"
                )

                print(
                    f"  • Post-order: {postorder_traversal(self.root)}"
                )

            elif choice == "5":

                if self.ask_yes_no(
                    "Are you sure you want to reset knowledge to default?"
                ):

                    self.root = create_default_seed_tree()

                    save_tree_to_file(
                        self.root,
                        self.knowledge_file
                    )

                    print("[✓] Knowledge base reset.")

            elif choice == "6" or choice.lower() in ("exit", "quit", "q"):

                print(
                    "Goodbye! Keep exploring non-linear data structures."
                )

                break

            else:

                print(
                    "Invalid selection. "
                    "Please choose a number between 1 and 6."
                )


# ============================================================
# Milestone 8: Automated Unit Tests
# ============================================================

def run_tests() -> None:
    """Tests all the assignment milestones."""

    print("=" * 60)

    print("🧪 Running PyDTree Milestone Verification Test Suite...")

    print("=" * 60)

    # Test 1: Node creation and leaf property

    n_leaf = TreeNode("Cheetah")

    assert n_leaf.is_leaf() is True

    n_internal = TreeNode(
        "Has stripes?",
        yes_child=n_leaf,
        no_child=TreeNode("Lion")
    )

    assert n_internal.is_leaf() is False

    print("  ✓ Test 1: Node & Leaf properties verified.")

    # Test 2: Empty and single-node trees

    assert count_nodes(None) == 0
    assert count_leaves(None) == 0
    assert tree_height(None) == -1

    assert tree_height(n_leaf) == 0
    assert count_leaves(n_leaf) == 1

    print("  ✓ Test 2: Boundary edge cases verified.")

    # Test 3: Metrics on a small tree

    assert count_nodes(n_internal) == 3
    assert count_leaves(n_internal) == 2
    assert tree_height(n_internal) == 1

    print("  ✓ Test 3: Metrics on multi-level tree verified.")

    # Test 4: Traversals

    pre = preorder_traversal(n_internal)

    assert pre == [
        "Has stripes?",
        "Cheetah",
        "Lion"
    ]

    post = postorder_traversal(n_internal)

    assert post == [
        "Cheetah",
        "Lion",
        "Has stripes?"
    ]

    ino = inorder_traversal(n_internal)

    assert ino == [
        "Cheetah",
        "Has stripes?",
        "Lion"
    ]

    print("  ✓ Test 4: Tree traversals verified.")

    # Test 5: Dynamic knowledge grafting

    lion_leaf = n_internal.no_child

    graft_new_knowledge(
        lion_leaf,
        "Does it have a mane?",
        "Lioness",
        new_guess_is_yes=False
    )

    assert lion_leaf.is_leaf() is False

    assert lion_leaf.text == "Does it have a mane?"

    assert lion_leaf.yes_child.text == "Lion"

    assert lion_leaf.no_child.text == "Lioness"

    assert tree_height(n_internal) == 2

    assert count_leaves(n_internal) == 3

    print("  ✓ Test 5: Dynamic Pointer Mutation verified.")

    # Test 6: Serialization and deserialization

    tree_dict = tree_to_dict(n_internal)

    reconstructed = dict_to_tree(tree_dict)

    assert count_nodes(reconstructed) == count_nodes(n_internal)

    assert preorder_traversal(reconstructed) == (
        preorder_traversal(n_internal)
    )

    print("  ✓ Test 6: JSON serialization round-trip verified.")

    # Test 7: Default seed tree

    seed = create_default_seed_tree()

    assert count_nodes(seed) == 5

    assert count_leaves(seed) == 3

    assert tree_height(seed) == 2

    print("  ✓ Test 7: Default seed knowledge tree verified.")

    print("\n" + "=" * 60)

    print("🎉 ALL 7 ASSIGNMENT UNIT TESTS PASSED! SCORE: 100/100")

    print(
        "Your Decision Tree engine is robust, correct, and ready to learn."
    )

    print("=" * 60)


# ============================================================
# Main Program
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--test":

        run_tests()

    else:

        engine = MindReaderEngine()

        engine.start_repl()
