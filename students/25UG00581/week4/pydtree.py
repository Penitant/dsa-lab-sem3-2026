import json


# ============================================================
# MILESTONE 1: TREE NODE
# ============================================================

class TreeNode:
    def __init__(self, text: str, yes_child=None, no_child=None):
        self.text = text.strip()
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self) -> bool:
        """Return True if this node has no children."""
        return self.yes_child is None and self.no_child is None


# ============================================================
# MILESTONE 2: RECURSIVE METRICS
# ============================================================

def count_nodes(root):
    """Return total number of nodes."""
    if root is None:
        return 0

    return (
        1
        + count_nodes(root.yes_child)
        + count_nodes(root.no_child)
    )


def count_leaves(root):
    """Return total number of leaf nodes."""
    if root is None:
        return 0

    if root.is_leaf():
        return 1

    return (
        count_leaves(root.yes_child)
        + count_leaves(root.no_child)
    )


def tree_height(root):
    """Return tree height. Empty tree = -1."""
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

def preorder_traversal(root):
    """
    Root -> Yes subtree -> No subtree
    """
    if root is None:
        return []

    return (
        [root.text]
        + preorder_traversal(root.yes_child)
        + preorder_traversal(root.no_child)
    )


def inorder_traversal(root):
    """
    Yes subtree -> Root -> No subtree
    """
    if root is None:
        return []

    return (
        inorder_traversal(root.yes_child)
        + [root.text]
        + inorder_traversal(root.no_child)
    )


def postorder_traversal(root):
    """
    Yes subtree -> No subtree -> Root
    """
    if root is None:
        return []

    return (
        postorder_traversal(root.yes_child)
        + postorder_traversal(root.no_child)
        + [root.text]
    )


# ============================================================
# MILESTONE 4: SERIALIZATION
# ============================================================

def tree_to_dict(root):
    """
    Convert a TreeNode into a dictionary
    that can be stored as JSON.
    """

    if root is None:
        return None

    # Leaf node
    if root.is_leaf():
        return {
            "guess": root.text
        }

    # Question node
    return {
        "question": root.text,
        "yes": tree_to_dict(root.yes_child),
        "no": tree_to_dict(root.no_child)
    }


def dict_to_tree(data):
    """
    Convert a dictionary back into a TreeNode.
    """

    if data is None:
        return None

    # Leaf
    if "guess" in data:
        return TreeNode(data["guess"])

    # Question
    return TreeNode(
        data["question"],
        dict_to_tree(data["yes"]),
        dict_to_tree(data["no"])
    )


# ============================================================
# MILESTONE 5: POINTER GRAFTING
# ============================================================

def graft_new_knowledge(
    leaf_node: TreeNode,
    new_question: str,
    new_guess: str,
    new_guess_is_yes: bool,
) -> None:

    # Remember the old guess
    old_guess = leaf_node.text

    # Create the two new leaves
    new_guess_node = TreeNode(new_guess)
    old_guess_node = TreeNode(old_guess)

    # Change the old leaf into a question
    leaf_node.text = new_question

    # Connect the children
    if new_guess_is_yes:
        leaf_node.yes_child = new_guess_node
        leaf_node.no_child = old_guess_node
    else:
        leaf_node.yes_child = old_guess_node
        leaf_node.no_child = new_guess_node


# ============================================================
# MILESTONE 6: ASCII TREE
# ============================================================

def print_ascii_tree(root):
    """
    Print the tree using ASCII connectors.
    """

    if root is None:
        print("(empty tree)")
        return

    def print_node(node, prefix="", is_last=True, branch=""):
        if node.is_leaf():
            symbol = "[★]"
        else:
            symbol = "[?]"

        connector = "└── " if is_last else "├── "

        print(prefix + connector + symbol + " " + node.text)

        if node.is_leaf():
            return

        children = [
            ("YES", node.yes_child),
            ("NO", node.no_child)
        ]

        for i, (label, child) in enumerate(children):
            last = i == len(children) - 1

            if child is not None:
                if is_last:
                    new_prefix = prefix + "    "
                else:
                    new_prefix = prefix + "│   "

                print_node(
                    child,
                    new_prefix,
                    last,
                    label
                )

    print_node(root)


# ============================================================
# DEFAULT SEED TREE
# ============================================================

def create_default_tree():
    """
    Create the starting knowledge tree.
    """

    dolphin = TreeNode("Dolphin")
    dog = TreeNode("Dog")
    elephant = TreeNode("Elephant")

    bark_question = TreeNode(
        "Does it bark?",
        dog,
        elephant
    )

    root = TreeNode(
        "Does it live in water?",
        dolphin,
        bark_question
    )

    return root


# ============================================================
# MIND READER ENGINE
# ============================================================

class MindReaderEngine:

    def __init__(self):
        self.root = create_default_tree()

    # --------------------------------------------------------
    # PLAY GAME
    # --------------------------------------------------------

    def play(self):

        current = self.root

        while not current.is_leaf():

            print()
            print(current.text)

            answer = input("Enter yes/no: ").strip().lower()

            if answer in ("yes", "y"):
                current = current.yes_child

            elif answer in ("no", "n"):
                current = current.no_child

            else:
                print("Please enter yes or no.")

        # Computer reached a guess
        print()
        print("My guess is:", current.text)

        correct = input("Am I correct? (yes/no): ").strip().lower()

        if correct in ("yes", "y"):
            print("Great! I got it right.")

        elif correct in ("no", "n"):
            print()
            print("I want to learn.")

            new_guess = input(
                "What was your animal/object? "
            ).strip()

            new_question = input(
                f"Give me a question that distinguishes "
                f"{new_guess} from {current.text}: "
            ).strip()

            answer_for_new_guess = input(
                f"For {new_guess}, is the answer to "
                f"'{new_question}' yes or no? "
            ).strip().lower()

            new_guess_is_yes = (
                answer_for_new_guess in ("yes", "y")
            )

            graft_new_knowledge(
                current,
                new_question,
                new_guess,
                new_guess_is_yes
            )

            print()
            print("Knowledge updated successfully!")

        else:
            print("Please enter yes or no.")

    # --------------------------------------------------------
    # DISPLAY TREE
    # --------------------------------------------------------

    def display_tree(self):

        print()
        print("========== VISUAL TREE ==========")
        print_ascii_tree(self.root)

    # --------------------------------------------------------
    # ANALYTICS
    # --------------------------------------------------------

    def analytics(self):

        print()
        print("========== TREE ANALYTICS ==========")

        print("Height      :", tree_height(self.root))
        print("Leaves      :", count_leaves(self.root))
        print("Total Nodes :", count_nodes(self.root))

    # --------------------------------------------------------
    # TRAVERSALS
    # --------------------------------------------------------

    def traversals(self):

        print()
        print("========== TRAVERSALS ==========")

        print("\nPre-order:")
        for item in preorder_traversal(self.root):
            print(item)

        print("\nIn-order:")
        for item in inorder_traversal(self.root):
            print(item)

        print("\nPost-order:")
        for item in postorder_traversal(self.root):
            print(item)

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    def reset(self):

        self.root = create_default_tree()

        print()
        print("Tree has been reset to the default seed.")

    # --------------------------------------------------------
    # SAVE TREE
    # --------------------------------------------------------

    def save_tree(self):

        data = tree_to_dict(self.root)

        with open("tree.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Tree saved successfully to tree.json")

    # --------------------------------------------------------
    # LOAD TREE
    # --------------------------------------------------------

    def load_tree(self):

        try:
            with open("tree.json", "r") as file:
                data = json.load(file)

            self.root = dict_to_tree(data)

            print("Tree loaded successfully.")

        except FileNotFoundError:
            print("tree.json not found. Using default tree.")

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    def run(self):

        while True:

            print()
            print("===================================")
            print("       MIND READER ENGINE")
            print("===================================")
            print("1. Play 20-Questions")
            print("2. Display Visual Tree")
            print("3. View Tree Analytics")
            print("4. View Traversals")
            print("5. Reset to Default Seed")
            print("6. Save Tree")
            print("7. Load Tree")
            print("8. Exit")
            print("===================================")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.play()

            elif choice == "2":
                self.display_tree()

            elif choice == "3":
                self.analytics()

            elif choice == "4":
                self.traversals()

            elif choice == "5":
                self.reset()

            elif choice == "6":
                self.save_tree()

            elif choice == "7":
                self.load_tree()

            elif choice == "8":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    engine = MindReaderEngine()
    engine.run()

