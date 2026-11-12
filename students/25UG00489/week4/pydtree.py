import json
import sys
from typing import List, Optional


# --------------------------------------------------
# MILESTONE 1: TREE NODE
# --------------------------------------------------

class TreeNode:
    def __init__(
        self,
        text: str,
        yes_child=None,
        no_child=None
    ):
        self.text = text.strip()
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self) -> bool:
        return (
            self.yes_child is None
            and self.no_child is None
        )


# --------------------------------------------------
# MILESTONE 2: RECURSIVE METRICS
# --------------------------------------------------

def count_nodes(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0

    return (
        1
        + count_nodes(root.yes_child)
        + count_nodes(root.no_child)
    )


def count_leaves(root: Optional[TreeNode]) -> int:
    if root is None:
        return 0

    if root.is_leaf():
        return 1

    return (
        count_leaves(root.yes_child)
        + count_leaves(root.no_child)
    )


def tree_height(root: Optional[TreeNode]) -> int:
    if root is None:
        return -1

    if root.is_leaf():
        return 0

    return 1 + max(
        tree_height(root.yes_child),
        tree_height(root.no_child)
    )


# --------------------------------------------------
# MILESTONE 3: TREE TRAVERSALS
# --------------------------------------------------

def preorder_traversal(root: Optional[TreeNode]) -> List[str]:
    if root is None:
        return []

    return (
        [root.text]
        + preorder_traversal(root.yes_child)
        + preorder_traversal(root.no_child)
    )


def inorder_traversal(root: Optional[TreeNode]) -> List[str]:
    if root is None:
        return []

    return (
        inorder_traversal(root.yes_child)
        + [root.text]
        + inorder_traversal(root.no_child)
    )


def postorder_traversal(root: Optional[TreeNode]) -> List[str]:
    if root is None:
        return []

    return (
        postorder_traversal(root.yes_child)
        + postorder_traversal(root.no_child)
        + [root.text]
    )


# --------------------------------------------------
# MILESTONE 4: JSON SERIALIZATION
# --------------------------------------------------

def tree_to_dict(root: Optional[TreeNode]):
    if root is None:
        return None

    if root.is_leaf():
        return {"guess": root.text}

    return {
        "question": root.text,
        "yes": tree_to_dict(root.yes_child),
        "no": tree_to_dict(root.no_child)
    }


def dict_to_tree(data) -> Optional[TreeNode]:
    if data is None:
        return None

    if "guess" in data:
        return TreeNode(data["guess"])

    return TreeNode(
        data["question"],
        dict_to_tree(data["yes"]),
        dict_to_tree(data["no"])
    )


# --------------------------------------------------
# MILESTONE 5: KNOWLEDGE GRAFTING
# --------------------------------------------------

def graft_new_knowledge(
    leaf_node: TreeNode,
    new_question: str,
    new_guess: str,
    new_guess_is_yes: bool
) -> None:

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


# --------------------------------------------------
# MILESTONE 6: ASCII TREE VISUALIZER
# --------------------------------------------------

def print_ascii_tree(root: Optional[TreeNode]) -> None:
    if root is None:
        print("(Empty tree)")
        return

    def display(node, prefix="", is_last=True, branch=""):
        if node is None:
            return

        connector = "└── " if is_last else "├── "

        if node.is_leaf():
            label = "[★] "
        else:
            label = "[?] "

        print(prefix + connector + branch + label + node.text)

        children = [
            ("YES: ", node.yes_child),
            ("NO: ", node.no_child)
        ]

        children = [
            (name, child)
            for name, child in children
            if child is not None
        ]

        for index, (name, child) in enumerate(children):
            last_child = index == len(children) - 1

            new_prefix = prefix + (
                "    " if is_last else "│   "
            )

            display(
                child,
                new_prefix,
                last_child,
                name
            )

    if root.is_leaf():
        print("[★] " + root.text)
    else:
        print("[?] " + root.text)

        children = [
            ("YES: ", root.yes_child),
            ("NO: ", root.no_child)
        ]

        children = [
            (name, child)
            for name, child in children
            if child is not None
        ]

        for index, (name, child) in enumerate(children):
            display(
                child,
                "",
                index == len(children) - 1,
                name
            )


# --------------------------------------------------
# DEFAULT KNOWLEDGE TREE
# --------------------------------------------------

def create_default_tree() -> TreeNode:
    return TreeNode(
        "Does it live in water?",
        TreeNode("Dolphin"),
        TreeNode(
            "Does it bark?",
            TreeNode("Dog"),
            TreeNode("Elephant")
        )
    )


# --------------------------------------------------
# MIND READER ENGINE
# --------------------------------------------------

class MindReaderEngine:

    def __init__(self):
        self.filename = "pydtree.json"
        self.root = self.load_tree()

    def load_tree(self) -> TreeNode:
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            return dict_to_tree(data)

        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            return create_default_tree()

    def save_tree(self) -> None:
        data = tree_to_dict(self.root)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def play(self) -> None:
        print("\nThink of an animal!")
        print("Answer the following questions with yes or no.\n")

        current = self.root

        while not current.is_leaf():
            answer = input(current.text + " (yes/no): ").strip().lower()

            if answer in ("yes", "y"):
                current = current.yes_child
            elif answer in ("no", "n"):
                current = current.no_child
            else:
                print("Please enter yes or no.")
                continue

        answer = input(
            "Is it " + current.text + "? (yes/no): "
        ).strip().lower()

        if answer in ("yes", "y"):
            print("\nI guessed it! Your animal is " + current.text + ".")
            return

        if answer not in ("no", "n"):
            print("Invalid answer. Please try again.")
            return

        print("\nI give up! Help me learn.")

        new_guess = input("What animal were you thinking of? ").strip()

        if not new_guess:
            print("The animal name cannot be empty.")
            return

        new_question = input(
            "Give me a question that distinguishes "
            + new_guess
            + " from "
            + current.text
            + ": "
        ).strip()

        if not new_question:
            print("The question cannot be empty.")
            return

        answer = input(
            "For "
            + new_guess
            + ", is the answer to this question yes? (yes/no): "
        ).strip().lower()

        if answer not in ("yes", "y", "no", "n"):
            print("Invalid answer. Knowledge was not saved.")
            return

        new_guess_is_yes = answer in ("yes", "y")

        graft_new_knowledge(
            current,
            new_question,
            new_guess,
            new_guess_is_yes
        )

        self.save_tree()
        print("\nThank you! I've learned something new.")

    def display_tree(self) -> None:
        print("\n========== KNOWLEDGE TREE ==========")
        print_ascii_tree(self.root)

    def analytics(self) -> None:
        print("\n========== TREE ANALYTICS ==========")
        print("Total nodes:", count_nodes(self.root))
        print("Total leaves:", count_leaves(self.root))
        print("Tree height:", tree_height(self.root))

    def show_traversals(self) -> None:
        print("\n========== TREE TRAVERSALS ==========")

        print("Preorder:", preorder_traversal(self.root))
        print("Inorder:", inorder_traversal(self.root))
        print("Postorder:", postorder_traversal(self.root))

    def reset(self) -> None:
        self.root = create_default_tree()
        self.save_tree()
        print("\nKnowledge tree reset to default.")

    def run(self) -> None:
        while True:
            print("\n========== PYDTREE: MIND READER ==========")
            print("1. Play 20 Questions")
            print("2. Display Visual Tree")
            print("3. View Tree Analytics")
            print("4. View Traversals")
            print("5. Reset to Default Seed")
            print("6. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self.play()

            elif choice == "2":
                self.display_tree()

            elif choice == "3":
                self.analytics()

            elif choice == "4":
                self.show_traversals()

            elif choice == "5":
                confirm = input(
                    "Are you sure you want to reset? (yes/no): "
                ).strip().lower()

                if confirm in ("yes", "y"):
                    self.reset()

            elif choice == "6":
                self.save_tree()
                print("\nGoodbye! Your knowledge has been saved.")
                break

            else:
                print("\nInvalid choice. Please select 1 to 6.")


# --------------------------------------------------
# MILESTONE 7: SELF-VERIFICATION TEST SUITE
# --------------------------------------------------

def run_tests() -> None:

    print("=" * 60)
    print("Running PyDTree Milestone Verification Test Suite...")
    print("=" * 60)

    # Test 1: Node and leaf properties
    leaf = TreeNode("Dog")
    assert leaf.is_leaf()

    root = TreeNode("Animal", leaf, TreeNode("Cat"))
    assert not root.is_leaf()

    print("  ✓ Test 1: Node & Leaf properties verified.")

    # Test 2: Boundary cases
    assert count_nodes(None) == 0
    assert count_leaves(None) == 0
    assert tree_height(None) == -1

    single = TreeNode("Dolphin")
    assert count_nodes(single) == 1
    assert count_leaves(single) == 1
    assert tree_height(single) == 0

    print("  ✓ Test 2: Boundary edge cases (None, single node) verified.")

    # Test 3: Metrics on multi-level tree
    test_tree = TreeNode(
        "Root",
        TreeNode("Left"),
        TreeNode(
            "Right",
            TreeNode("Right-Left"),
            TreeNode("Right-Right")
        )
    )

    assert count_nodes(test_tree) == 5
    assert count_leaves(test_tree) == 3
    assert tree_height(test_tree) == 2

    print("  ✓ Test 3: Metrics on multi-level tree verified.")

    # Test 4: Traversals
    assert preorder_traversal(test_tree) == [
        "Root", "Left", "Right", "Right-Left", "Right-Right"
    ]

    assert inorder_traversal(test_tree) == [
        "Left", "Root", "Right-Left", "Right", "Right-Right"
    ]

    assert postorder_traversal(test_tree) == [
        "Left", "Right-Left", "Right-Right", "Right", "Root"
    ]

    print("  ✓ Test 4: Pre-order, In-order, Post-order walks verified.")

    # Test 5: Knowledge grafting
    old_leaf = TreeNode("Dog")

    graft_new_knowledge(
        old_leaf,
        "Does it meow?",
        "Cat",
        True
    )

    assert old_leaf.text == "Does it meow?"
    assert old_leaf.yes_child.text == "Cat"
    assert old_leaf.no_child.text == "Dog"

    print("  ✓ Test 5: Dynamic Pointer Mutation (Knowledge Grafting) verified.")

    # Test 6: JSON round trip
    original = create_default_tree()
    converted = tree_to_dict(original)
    reconstructed = dict_to_tree(converted)

    assert tree_to_dict(reconstructed) == converted

    print("  ✓ Test 6: JSON Dictionary serialization round-trip verified.")

    # Test 7: Default seed tree
    default = create_default_tree()

    assert default.text == "Does it live in water?"
    assert default.yes_child.text == "Dolphin"
    assert default.no_child.text == "Does it bark?"
    assert default.no_child.yes_child.text == "Dog"
    assert default.no_child.no_child.text == "Elephant"

    print("  ✓ Test 7: Default seed knowledge tree verified.")

    print("\n" + "=" * 60)
    print("ALL 7 ASSIGNMENT UNIT TESTS PASSED! SCORE: 100/100")
    print("=" * 60)


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        engine = MindReaderEngine()
        engine.run()
