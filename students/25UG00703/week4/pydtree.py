
"""
PyDTree - Build an Adaptive 20-Questions Engine
Week 4 Assignment
Python 3
"""

import sys
import json
from pathlib import Path


# ============================================================
# MILESTONE 1: TREE NODE
# ============================================================

class TreeNode:

    def __init__(self, text, yes_child=None, no_child=None):
        self.text = text
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self):
        return self.yes_child is None and self.no_child is None


# ============================================================
# MILESTONE 2: RECURSIVE METRICS
# ============================================================

def count_nodes(root):
    """Count all nodes in the tree."""

    if root is None:
        return 0

    return (
        1
        + count_nodes(root.yes_child)
        + count_nodes(root.no_child)
    )


def count_leaves(root):
    """Count all leaf nodes."""

    if root is None:
        return 0

    if root.is_leaf():
        return 1

    return (
        count_leaves(root.yes_child)
        + count_leaves(root.no_child)
    )


def tree_height(root):
    """Calculate tree height. Empty tree = -1."""

    if root is None:
        return -1

    return 1 + max(
        tree_height(root.yes_child),
        tree_height(root.no_child)
    )


# ============================================================
# MILESTONE 3: TREE TRAVERSALS
# ============================================================

def preorder_traversal(root):
    """Root, Left, Right."""

    if root is None:
        return []

    return (
        [root.text]
        + preorder_traversal(root.yes_child)
        + preorder_traversal(root.no_child)
    )


def inorder_traversal(root):
    """Left, Root, Right."""

    if root is None:
        return []

    return (
        inorder_traversal(root.yes_child)
        + [root.text]
        + inorder_traversal(root.no_child)
    )


def postorder_traversal(root):
    """Left, Right, Root."""

    if root is None:
        return []

    return (
        postorder_traversal(root.yes_child)
        + postorder_traversal(root.no_child)
        + [root.text]
    )


# ============================================================
# MILESTONE 4: JSON SERIALIZATION
# ============================================================

def tree_to_dict(root):
    """Convert tree into nested dictionary."""

    if root is None:
        return None

    if root.is_leaf():
        return {"guess": root.text}

    return {
        "question": root.text,
        "yes": tree_to_dict(root.yes_child),
        "no": tree_to_dict(root.no_child)
    }


def dict_to_tree(data):
    """Convert dictionary back into a tree."""

    if data is None:
        return None

    if not isinstance(data, dict):
        raise ValueError("Tree data must be a dictionary.")

    if "guess" in data:
        return TreeNode(data["guess"])

    if "question" in data:
        if "yes" not in data or "no" not in data:
            raise ValueError("Missing question branches.")

        return TreeNode(
            data["question"],
            dict_to_tree(data["yes"]),
            dict_to_tree(data["no"])
        )

    raise ValueError("Invalid tree dictionary.")


# ============================================================
# MILESTONE 5: KNOWLEDGE GRAFTING
# ============================================================

def graft_new_knowledge(
    leaf_node,
    new_question,
    new_guess,
    new_guess_is_yes
):
    """Replace an incorrect leaf guess with a new question."""

    if not isinstance(leaf_node, TreeNode) or not leaf_node.is_leaf():
        raise ValueError("Knowledge can only be added to a leaf.")

    new_question = new_question.strip()
    new_guess = new_guess.strip()

    if not new_question or not new_guess:
        raise ValueError("Question and guess cannot be empty.")

    old_guess = leaf_node.text

    new_guess_node = TreeNode(new_guess)
    old_guess_node = TreeNode(old_guess)

    leaf_node.text = new_question

    if new_guess_is_yes:
        leaf_node.yes_child = new_guess_node
        leaf_node.no_child = old_guess_node
    else:
        leaf_node.yes_child = old_guess_node
        leaf_node.no_child = new_guess_node


# ============================================================
# MILESTONE 6: ASCII TREE VISUALIZATION
# ============================================================

def print_ascii_tree(root):
    """Display the decision tree."""

    if root is None:
        print("(Empty tree)")
        return

    def display(node, prefix="", is_last=True):
        if node is None:
            return

        connector = "└── " if is_last else "├── "
        node_type = "[LEAF]" if node.is_leaf() else "[QUESTION]"

        print(prefix + connector + node_type + " " + node.text)

        children = []

        if node.yes_child is not None:
            children.append(("YES", node.yes_child))

        if node.no_child is not None:
            children.append(("NO", node.no_child))

        for index, (label, child) in enumerate(children):
            last = index == len(children) - 1

            branch_prefix = prefix + (
                "    " if is_last else "│   "
            )

            branch_connector = "└── " if last else "├── "

            print(branch_prefix + branch_connector + label)

            display(
                child,
                branch_prefix + ("    " if last else "│   "),
                True
            )

    print("\nTREE STRUCTURE")
    print("=" * 40)

    node_type = "[LEAF]" if root.is_leaf() else "[QUESTION]"
    print(node_type + " " + root.text)

    children = []

    if root.yes_child is not None:
        children.append(("YES", root.yes_child))

    if root.no_child is not None:
        children.append(("NO", root.no_child))

    for index, (label, child) in enumerate(children):
        last = index == len(children) - 1

        print(("└── " if last else "├── ") + label)

        display(child, "    " if last else "│   ", True)

    print("=" * 40)


# ============================================================
# DEFAULT KNOWLEDGE TREE
# ============================================================

def create_default_tree():

    return TreeNode(
        "Does it live in water?",
        TreeNode("Dolphin"),
        TreeNode(
            "Does it bark?",
            TreeNode("Dog"),
            TreeNode("Elephant")
        )
    )


# ============================================================
# GAME ENGINE
# ============================================================

class MindReaderEngine:

    def __init__(self):

        self.root = create_default_tree()

        self.save_file = Path(__file__).with_name(
            "pydtree_tree.json"
        )

        self.load_tree()

    def save_tree(self):
        """Save knowledge to a JSON file."""

        try:
            with self.save_file.open("w", encoding="utf-8") as file:
                json.dump(tree_to_dict(self.root), file, indent=4)

        except (OSError, TypeError, ValueError) as error:
            print("Saving error:", error)

    def load_tree(self):
        """Load previously saved knowledge."""

        if not self.save_file.exists():
            return

        try:
            with self.save_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.root = dict_to_tree(data)

        except (OSError, json.JSONDecodeError, ValueError) as error:
            print("Loading error:", error)
            self.root = create_default_tree()

    def play_game(self):
        """Play the adaptive 20 Questions game."""

        print("\nThink of an animal!")

        current = self.root

        while not current.is_leaf():

            print("\n" + current.text)

            answer = input("Your answer (yes/no): ").strip().lower()

            if answer in ("yes", "y"):
                current = current.yes_child

            elif answer in ("no", "n"):
                current = current.no_child

            else:
                print("Please enter yes or no.")

        print("\nMy guess is:", current.text)

        answer = input("Am I correct? (yes/no): ").strip().lower()

        if answer in ("yes", "y"):
            print("Great! I guessed correctly!")
            return

        if answer not in ("no", "n"):
            print("Invalid answer.")
            return

        old_guess = current.text

        new_guess = input(
            "What animal were you thinking of? "
        ).strip()

        if not new_guess:
            print("Animal name cannot be empty.")
            return

        new_question = input(
            f"Give me a question that distinguishes "
            f"{new_guess} from {old_guess}: "
        ).strip()

        if not new_question:
            print("Question cannot be empty.")
            return

        answer = input(
            f"For {new_guess}, is the answer YES? (yes/no): "
        ).strip().lower()

        if answer in ("yes", "y"):
            new_guess_is_yes = True

        elif answer in ("no", "n"):
            new_guess_is_yes = False

        else:
            print("Invalid answer.")
            return

        graft_new_knowledge(
            current,
            new_question,
            new_guess,
            new_guess_is_yes
        )

        self.save_tree()

        print("\nThank you! I learned something new.")

    def display_analytics(self):
        """Display tree statistics."""

        print("\nTREE ANALYTICS")
        print("-" * 35)

        print("Total nodes:", count_nodes(self.root))
        print("Total leaves:", count_leaves(self.root))
        print("Tree height:", tree_height(self.root))

    def display_traversals(self):
        """Display tree traversal results."""

        print("\nTREE TRAVERSALS")

        print("Preorder:", preorder_traversal(self.root))
        print("Inorder:", inorder_traversal(self.root))
        print("Postorder:", postorder_traversal(self.root))

    def reset_tree(self):
        """Restore original knowledge."""

        self.root = create_default_tree()
        self.save_tree()

        print("\nTree reset successfully!")

    def run(self):
        """Main game menu."""

        print("\n================================")
        print("  PyDTree - 20 Questions Engine")
        print("================================")

        while True:

            print("\n1. Play 20 Questions")
            print("2. Display Visual Tree")
            print("3. View Tree Analytics")
            print("4. View Traversals")
            print("5. Reset to Default Seed")
            print("6. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self.play_game()

            elif choice == "2":
                print_ascii_tree(self.root)

            elif choice == "3":
                self.display_analytics()

            elif choice == "4":
                self.display_traversals()

            elif choice == "5":
                self.reset_tree()

            elif choice == "6":
                self.save_tree()
                print("\nThank you for playing!")
                break

            else:
                print("Invalid choice. Select 1-6.")


# ============================================================
# SEVEN SELF-VERIFICATION TESTS
# ============================================================

def run_tests():

    print("\nPYDTREE VERIFICATION TESTS")
    print("=" * 45)

    tests = []

    def test_node():
        root = TreeNode("Animal")
        assert root.text == "Animal"
        assert root.is_leaf()

        root.yes_child = TreeNode("Dog")
        assert not root.is_leaf()

    tests.append(("TreeNode properties", test_node))

    def test_boundaries():
        assert count_nodes(None) == 0
        assert count_leaves(None) == 0
        assert tree_height(None) == -1

        leaf = TreeNode("Cat")

        assert count_nodes(leaf) == 1
        assert count_leaves(leaf) == 1
        assert tree_height(leaf) == 0

    tests.append(("Boundary cases", test_boundaries))

    def test_metrics():
        root = create_default_tree()

        assert count_nodes(root) == 5
        assert count_leaves(root) == 3
        assert tree_height(root) == 2

    tests.append(("Recursive metrics", test_metrics))

    def test_traversals():
        root = create_default_tree()

        assert preorder_traversal(root) == [
            "Does it live in water?",
            "Dolphin",
            "Does it bark?",
            "Dog",
            "Elephant"
        ]

        assert inorder_traversal(root) == [
            "Dolphin",
            "Does it live in water?",
            "Dog",
            "Does it bark?",
            "Elephant"
        ]

        assert postorder_traversal(root) == [
            "Dolphin",
            "Dog",
            "Elephant",
            "Does it bark?",
            "Does it live in water?"
        ]

    tests.append(("Tree traversals", test_traversals))

    def test_grafting():
        leaf = TreeNode("Dog")

        graft_new_knowledge(
            leaf,
            "Does it have feathers?",
            "Parrot",
            True
        )

        assert leaf.text == "Does it have feathers?"
        assert leaf.yes_child.text == "Parrot"
        assert leaf.no_child.text == "Dog"

        another_leaf = TreeNode("Cat")

        graft_new_knowledge(
            another_leaf,
            "Does it bark?",
            "Dog",
            False
        )

        assert another_leaf.yes_child.text == "Cat"
        assert another_leaf.no_child.text == "Dog"

    tests.append(("Knowledge grafting", test_grafting))

    def test_serialization():
        original = create_default_tree()

        data = tree_to_dict(original)
        restored = dict_to_tree(data)

        assert tree_to_dict(restored) == data
        assert count_nodes(restored) == count_nodes(original)

        json_data = json.dumps(data)
        restored_again = dict_to_tree(json.loads(json_data))

        assert tree_to_dict(restored_again) == data

    tests.append(("JSON serialization", test_serialization))

    def test_default_tree():
        root = create_default_tree()

        assert root.text == "Does it live in water?"
        assert root.yes_child.text == "Dolphin"
        assert root.no_child.text == "Does it bark?"
        assert root.no_child.yes_child.text == "Dog"
        assert root.no_child.no_child.text == "Elephant"

    tests.append(("Default knowledge tree", test_default_tree))

    passed = 0

    for index, (name, function) in enumerate(tests, 1):

        try:
            function()
            print(f"[PASS] Test {index}: {name}")
            passed += 1

        except Exception as error:
            print(f"[FAIL] Test {index}: {name}")
            print("Error:", error)

    print("=" * 45)

    if passed == 7:
        print("ALL 7 ASSIGNMENT UNIT TESTS PASSED!")
        print("SCORE: 100/100")
    else:
        print(f"{passed}/7 TESTS PASSED")
        print(f"SCORE: {passed / 7 * 100:.0f}/100")

    print("=" * 45)

    return passed == 7


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    if "--test" in sys.argv:

        success = run_tests()
        sys.exit(0 if success else 1)

    else:

        engine = MindReaderEngine()

        try:
            engine.run()

        except (KeyboardInterrupt, EOFError):
            engine.save_tree()
            print("\nProgram closed. Goodbye!")
