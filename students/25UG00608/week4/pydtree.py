import sys
from typing import List, Optional


# ============================================================
# MILESTONE 1: TREE NODE
# ============================================================

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


# ============================================================
# MILESTONE 2: RECURSIVE TREE METRICS
# ============================================================

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


# ============================================================
# MILESTONE 3: TREE TRAVERSALS
# ============================================================

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


# ============================================================
# MILESTONE 4: JSON SERIALIZATION
# ============================================================

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


def save_tree(root: TreeNode, filename: str = "pydtree.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(tree_to_dict(root), file, indent=4)


def load_tree(filename: str = "pydtree.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return dict_to_tree(data)
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


# ============================================================
# MILESTONE 5: POINTER GRAFTING
# ============================================================

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


# ============================================================
# MILESTONE 6: ASCII TREE VISUALIZER
# ============================================================

def print_ascii_tree(root: Optional[TreeNode]) -> None:
    if root is None:
        print("(Empty tree)")
        return

    def display(node, prefix="", is_last=True, branch=""):
        if node.is_leaf():
            label = "[★] " + node.text
        else:
            label = "[?] " + node.text

        if prefix == "":
            print(label)
        else:
            connector = "└── " if is_last else "├── "
            print(prefix + connector + branch + label)

        children = []

        if node.yes_child is not None:
            children.append(("YES: ", node.yes_child))

        if node.no_child is not None:
            children.append(("NO: ", node.no_child))

        for index, (direction, child) in enumerate(children):
            last = index == len(children) - 1

            if prefix == "":
                new_prefix = ""
            else:
                new_prefix = prefix + (
                    "    " if is_last else "│   "
                )

            if prefix == "":
                display(
                    child,
                    "    ",
                    last,
                    direction
                )
            else:
                display(
                    child,
                    new_prefix,
                    last,
                    direction
                )

    display(root)


# ============================================================
# DEFAULT SEED KNOWLEDGE TREE
# ============================================================

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


# ============================================================
# MILESTONE 6: MIND READER ENGINE
# ============================================================

class MindReaderEngine:

    def __init__(self):
        self.filename = "pydtree.json"

        self.root = load_tree(self.filename)

        if self.root is None:
            self.root = create_default_tree()

    def play_game(self):
        print("\nThink of an animal!")
        current = self.root

        while not current.is_leaf():
            answer = input(
                current.text + " (yes/no): "
            ).strip().lower()

            if answer in ("yes", "y"):
                current = current.yes_child
            elif answer in ("no", "n"):
                current = current.no_child
            else:
                print("Please enter yes or no.")
                continue

        print("\nMy guess is:", current.text)

        correct = input(
            "Am I correct? (yes/no): "
        ).strip().lower()

        if correct in ("yes", "y"):
            print("Great! I guessed correctly!")
            return

        print("\nI learned something new!")

        new_guess = input(
            "What animal were you thinking of? "
        ).strip()

        if not new_guess:
            print("Empty guess. No changes made.")
            return

        new_question = input(
            "Give me a question that distinguishes "
            + new_guess + " from " + current.text + ": "
        ).strip()

        if not new_question:
            print("Empty question. No changes made.")
            return

        answer = input(
            "For " + new_guess +
            ", is the answer to this question yes or no? "
        ).strip().lower()

        if answer not in ("yes", "y", "no", "n"):
            print("Invalid answer. No changes made.")
            return

        new_guess_is_yes = answer in ("yes", "y")

        graft_new_knowledge(
            current,
            new_question,
            new_guess,
            new_guess_is_yes
        )

        save_tree(self.root, self.filename)

        print("\nKnowledge successfully updated and saved!")

    def display_tree(self):
        print("\n========== KNOWLEDGE TREE ==========")
        print_ascii_tree(self.root)

    def show_analytics(self):
        print("\n========== TREE ANALYTICS ==========")
        print("Total Nodes :", count_nodes(self.root))
        print("Leaf Nodes  :", count_leaves(self.root))
        print("Tree Height :", tree_height(self.root))

    def show_traversals(self):
        print("\n========== TREE TRAVERSALS ==========")

        print("Pre-order :",
              preorder_traversal(self.root))

        print("In-order  :",
              inorder_traversal(self.root))

        print("Post-order:",
              postorder_traversal(self.root))

    def reset_tree(self):
        self.root = create_default_tree()
        save_tree(self.root, self.filename)
        print("\nKnowledge tree reset to default!")

    def run(self):
        while True:
            print("\n================================")
            print("       PYDTREE MIND READER")
            print("================================")
            print("1. Play 20-Questions")
            print("2. Display Visual Tree")
            print("3. View Tree Analytics")
            print("4. View Traversals")
            print("5. Reset to Default Seed")
            print("6. Exit")
            print("================================")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.play_game()

            elif choice == "2":
                self.display_tree()

            elif choice == "3":
                self.show_analytics()

            elif choice == "4":
                self.show_traversals()

            elif choice == "5":
                self.reset_tree()

            elif choice == "6":
                print("\nThank you for playing!")
                break

            else:
                print("Invalid choice. Please try again.")


# ============================================================
# MILESTONE 7: SELF-VERIFICATION TEST SUITE
# ============================================================

def run_tests():

    print("=" * 60)
    print(" Running PyDTree Milestone Verification Test Suite...")
    print("=" * 60)

    # Test 1: Node and leaf properties
    leaf = TreeNode("Dog")
    assert leaf.text == "Dog"
    assert leaf.is_leaf()

    question = TreeNode(
        "Does it bark?",
        TreeNode("Dog"),
        TreeNode("Cat")
    )

    assert not question.is_leaf()

    print("  ✓ Test 1: Node & Leaf properties verified.")

    # Test 2: Boundary edge cases
    assert count_nodes(None) == 0
    assert count_leaves(None) == 0
    assert tree_height(None) == -1

    assert count_nodes(leaf) == 1
    assert count_leaves(leaf) == 1
    assert tree_height(leaf) == 0

    assert preorder_traversal(None) == []
    assert inorder_traversal(None) == []
    assert postorder_traversal(None) == []

    print("  ✓ Test 2: Boundary edge cases (None, single node) verified.")

    # Test 3: Metrics on multi-level tree
    root = create_default_tree()

    assert count_nodes(root) == 5
    assert count_leaves(root) == 3
    assert tree_height(root) == 2

    print("  ✓ Test 3: Metrics on multi-level tree verified.")

    # Test 4: Tree traversals
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

    print("  ✓ Test 4: Pre-order, In-order, Post-order walks verified.")

    # Test 5: Pointer grafting
    old_leaf = TreeNode("Cat")

    graft_new_knowledge(
        old_leaf,
        "Does it swim?",
        "Fish",
        True
    )

    assert old_leaf.text == "Does it swim?"
    assert old_leaf.yes_child.text == "Fish"
    assert old_leaf.no_child.text == "Cat"
    assert not old_leaf.is_leaf()

    print("  ✓ Test 5: Dynamic Pointer Mutation (Knowledge Grafting) verified.")

    # Test 6: JSON serialization round-trip
    original = create_default_tree()

    converted = tree_to_dict(original)
    restored = dict_to_tree(converted)

    assert tree_to_dict(restored) == converted

    print("  ✓ Test 6: JSON Dictionary serialization round-trip verified.")

    # Test 7: Default seed knowledge tree
    seed = create_default_tree()

    assert seed.text == "Does it live in water?"
    assert seed.yes_child.text == "Dolphin"
    assert seed.no_child.text == "Does it bark?"
    assert seed.no_child.yes_child.text == "Dog"
    assert seed.no_child.no_child.text == "Elephant"

    print("  ✓ Test 7: Default seed knowledge tree verified.")

    print("\n" + "=" * 60)
    print(" ALL 7 ASSIGNMENT UNIT TESTS PASSED! SCORE: 100/100")
    print("=" * 60)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        game = MindReaderEngine()
        game.run()


