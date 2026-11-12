
import json
import argparse


# MILESTONE 1: TREE NODE

class TreeNode:
    def __init__(self, text: str, yes_child=None, no_child=None):
        self.text = text.strip()
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self) -> bool:
        return self.yes_child is None and self.no_child is None


# MILESTONE 2: RECURSIVE METRICS

def count_nodes(root):
    if root is None:
        return 0
    return 1 + count_nodes(root.yes_child) + count_nodes(root.no_child)


def count_leaves(root):
    if root is None:
        return 0
    if root.is_leaf():
        return 1
    return count_leaves(root.yes_child) + count_leaves(root.no_child)


def tree_height(root):
    if root is None:
        return -1
    if root.is_leaf():
        return 0
    return 1 + max(
        tree_height(root.yes_child),
        tree_height(root.no_child)
    )


# MILESTONE 3: TREE TRAVERSALS

def preorder_traversal(root):
    if root is None:
        return []
    return (
        [root.text]
        + preorder_traversal(root.yes_child)
        + preorder_traversal(root.no_child)
    )


def inorder_traversal(root):
    if root is None:
        return []
    return (
        inorder_traversal(root.yes_child)
        + [root.text]
        + inorder_traversal(root.no_child)
    )


def postorder_traversal(root):
    if root is None:
        return []
    return (
        postorder_traversal(root.yes_child)
        + postorder_traversal(root.no_child)
        + [root.text]
    )


# MILESTONE 4: JSON SERIALIZATION

def tree_to_dict(root):
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
    if data is None:
        return None

    if "guess" in data:
        return TreeNode(data["guess"])

    return TreeNode(
        data["question"],
        dict_to_tree(data["yes"]),
        dict_to_tree(data["no"])
    )


# MILESTONE 5: POINTER GRAFTING

def graft_new_knowledge(
    leaf_node: TreeNode,
    new_question: str,
    new_guess: str,
    new_guess_is_yes: bool,
) -> None:

    old_guess = leaf_node.text

    leaf_node.text = new_question.strip()

    new_leaf = TreeNode(new_guess.strip())
    old_leaf = TreeNode(old_guess)

    if new_guess_is_yes:
        leaf_node.yes_child = new_leaf
        leaf_node.no_child = old_leaf
    else:
        leaf_node.yes_child = old_leaf
        leaf_node.no_child = new_leaf


# DEFAULT SEED TREE

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


# MILESTONE 6: ASCII TREE VISUALIZER

def print_ascii_tree(root):
    if root is None:
        print("(Empty tree)")
        return

    def display(node, prefix="", is_last=True):
        connector = "└── " if is_last else "├── "
        symbol = "[★] " if node.is_leaf() else "[?] "

        print(prefix + connector + symbol + node.text)

        children = []
        if node.yes_child:
            children.append(("YES", node.yes_child))
        if node.no_child:
            children.append(("NO", node.no_child))

        for index, (label, child) in enumerate(children):
            last = index == len(children) - 1
            extension = "    " if is_last else "│   "
            print(prefix + extension + ("└── " if last else "├── ") + label)
            display(child, prefix + extension, True)

    symbol = "[★] " if root.is_leaf() else "[?] "
    print(symbol + root.text)

    children = []
    if root.yes_child:
        children.append(("YES", root.yes_child))
    if root.no_child:
        children.append(("NO", root.no_child))

    for index, (label, child) in enumerate(children):
        last = index == len(children) - 1
        print(("└── " if last else "├── ") + label)
        display(child, "    " if last else "│   ", True)


# MIND READER ENGINE

class MindReaderEngine:
    def __init__(self):
        self.root = create_default_tree()

    def play(self):
        node = self.root

        while not node.is_leaf():
            answer = input(node.text + " (yes/no): ").strip().lower()

            if answer in ("yes", "y"):
                node = node.yes_child
            elif answer in ("no", "n"):
                node = node.no_child
            else:
                print("Please enter yes or no.")
                continue

        answer = input(
            "Is your answer " + node.text + "? (yes/no): "
        ).strip().lower()

        if answer in ("yes", "y"):
            print("I guessed it!")
            return

        old_guess = node.text
        new_guess = input("What were you thinking of? ").strip()
        question = input(
            "Give me a question that distinguishes "
            + new_guess + " from " + old_guess + ": "
        ).strip()

        direction = input(
            "For " + new_guess + ", is the answer yes or no? "
        ).strip().lower()

        graft_new_knowledge(
            node,
            question,
            new_guess,
            direction in ("yes", "y")
        )

        print("Great! I learned something new.")

    def analytics(self):
        print("\nTree Analytics")
        print("Height:", tree_height(self.root))
        print("Leaves:", count_leaves(self.root))
        print("Total Nodes:", count_nodes(self.root))

    def traversals(self):
        print("\nPre-order:", preorder_traversal(self.root))
        print("In-order:", inorder_traversal(self.root))
        print("Post-order:", postorder_traversal(self.root))

    def run(self):
        while True:
            print("\n====== PYDTREE MIND READER ======")
            print("1. Play 20 Questions")
            print("2. Display Visual Tree")
            print("3. View Tree Analytics")
            print("4. View Traversals")
            print("5. Reset to Default Seed")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.play()
            elif choice == "2":
                print_ascii_tree(self.root)
            elif choice == "3":
                self.analytics()
            elif choice == "4":
                self.traversals()
            elif choice == "5":
                self.root = create_default_tree()
                print("Tree reset successfully.")
            elif choice == "6":
                print("Thank you for playing!")
                break
            else:
                print("Invalid choice. Try again.")


# SAVE AND LOAD KNOWLEDGE

def save_tree(root, filename="knowledge.json"):
    with open(filename, "w") as file:
        json.dump(tree_to_dict(root), file, indent=4)


def load_tree(filename="knowledge.json"):
    try:
        with open(filename, "r") as file:
            return dict_to_tree(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return create_default_tree()


# MAIN PROGRAM

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.test:
        print("Please run the instructor-provided test suite.")
        return

    game = MindReaderEngine()
    game.root = load_tree()
    game.run()
    save_tree(game.root)


if __name__ == "__main__":
    main()
