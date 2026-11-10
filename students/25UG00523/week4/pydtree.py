
import sys

# 1. TREE NODE

class TreeNode:
    def __init__(self, text, yes_child=None, no_child=None):
        self.text = text.strip()
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self):
        return self.yes_child is None and self.no_child is None

# 2. TREE METRICS

def count_nodes(root):
    if root is None:
        return 0

    return (1 + count_nodes(root.yes_child)
              + count_nodes(root.no_child))

def count_leaves(root):
    if root is None:
        return 0

    if root.is_leaf():
        return 1

    return (count_leaves(root.yes_child)
            + count_leaves(root.no_child))

def tree_height(root):
    if root is None:
        return -1

    return 1 + max(
        tree_height(root.yes_child),
        tree_height(root.no_child)
    )

# 3. TREE TRAVERSALS

def preorder(root):
    if root is None:
        return []

    return ([root.text]
            + preorder(root.yes_child)
            + preorder(root.no_child))

def inorder(root):
    if root is None:
        return []

    return (inorder(root.yes_child)
            + [root.text]
            + inorder(root.no_child))

def postorder(root):
    if root is None:
        return []

    return (postorder(root.yes_child)
            + postorder(root.no_child)
            + [root.text])

# 4. SERIALIZATION AND DESERIALIZATION

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

# 5. GRAFTING NEW KNOWLEDGE

def graft_new_knowledge(
    leaf_node,
    new_question,
    new_guess,
    new_guess_is_yes
):
    if not leaf_node.is_leaf():
        raise ValueError("Node must be a leaf.")

    old_guess = leaf_node.text

    new_leaf = TreeNode(new_guess)
    old_leaf = TreeNode(old_guess)

    leaf_node.text = new_question

    if new_guess_is_yes:
        leaf_node.yes_child = new_leaf
        leaf_node.no_child = old_leaf
    else:
        leaf_node.yes_child = old_leaf
        leaf_node.no_child = new_leaf

# 6. ASCII TREE VISUALIZER

def print_ascii_tree(root):
    if root is None:
        print("(empty tree)")
        return

    def display(node, prefix="", is_last=True):
        symbol = "[★]" if node.is_leaf() else "[?]"

        if prefix == "":
            print(symbol, node.text)
        else:
            connector = "└── " if is_last else "├── "
            print(prefix + connector + symbol + " " + node.text)

        children = []

        if node.yes_child is not None:
            children.append(("YES", node.yes_child))

        if node.no_child is not None:
            children.append(("NO", node.no_child))

        for i, (answer, child) in enumerate(children):
            last = i == len(children) - 1
            branch = "└── " if last else "├── "

            print(prefix + branch + answer + ":")

            new_prefix = prefix + ("    " if last else "│   ")
            display(child, new_prefix, True)

    display(root)

# 7. MIND READER ENGINE

class MindReaderEngine:

    def __init__(self):
        self.root = self.default_tree()

    def default_tree(self):
        return TreeNode(
            "Is it an animal?",
            TreeNode(
                "Can it fly?",
                TreeNode("Eagle"),
                TreeNode("Dog")
            ),
            TreeNode("Car")
        )

    def play(self):
        current = self.root

        if current is None:
            print("Tree is empty.")
            return

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

        print("My guess is:", current.text)

        correct = input(
            "Am I correct? (yes/no): "
        ).strip().lower()

        if correct not in ("yes", "y"):
            old_guess = current.text

            new_guess = input(
                "What were you thinking of? "
            ).strip()

            new_question = input(
                "Give a question that distinguishes "
                + new_guess + " from " + old_guess + ": "
            ).strip()

            answer = input(
                "Is the answer YES for " + new_guess + "? (yes/no): "
            ).strip().lower()

            if not new_guess or not new_question:
                print("Guess and question cannot be empty.")
                return

            graft_new_knowledge(
                current,
                new_question,
                new_guess,
                answer in ("yes", "y")
            )

            print("Thank you! I have learned something new.")

    def show_analytics(self):
        print("\nTREE ANALYTICS")
        print("Total nodes:", count_nodes(self.root))
        print("Leaf nodes:", count_leaves(self.root))
        print("Tree height:", tree_height(self.root))

    def show_traversals(self):
        print("\nPREORDER:", preorder(self.root))
        print("INORDER:", inorder(self.root))
        print("POSTORDER:", postorder(self.root))

    def reset(self):
        self.root = self.default_tree()
        print("Tree reset to default seed.")

    def run(self):
        while True:
            print("\n====== PYDTREE MIND READER ======")
            print("1. Play 20 Questions")
            print("2. Display Visual Tree")
            print("3. View Tree Analytics")
            print("4. View Traversals")
            print("5. Reset to default seed")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.play()
            elif choice == "2":
                print_ascii_tree(self.root)
            elif choice == "3":
                self.show_analytics()
            elif choice == "4":
                self.show_traversals()
            elif choice == "5":
                self.reset()
            elif choice == "6":
                print("Thank you for playing!")
                break
            else:
                print("Invalid choice. Please try again.")

# 8. AUTOMATED TESTS

def run_tests():

    # Test 1: TreeNode
    leaf = TreeNode(" Dog ")
    assert leaf.text == "Dog"
    assert leaf.is_leaf()

    # Test 2: Tree metrics
    root = TreeNode(
        "Animal?",
        TreeNode("Eagle"),
        TreeNode("Dog")
    )

    assert count_nodes(root) == 3
    assert count_leaves(root) == 2
    assert tree_height(root) == 1

    # Test 3: Traversals
    assert preorder(root) == [
        "Animal?", "Eagle", "Dog"
    ]

    assert inorder(root) == [
        "Eagle", "Animal?", "Dog"
    ]

    assert postorder(root) == [
        "Eagle", "Dog", "Animal?"
    ]

    # Test 4: Serialization
    data = tree_to_dict(root)

    assert data == {
        "question": "Animal?",
        "yes": {"guess": "Eagle"},
        "no": {"guess": "Dog"}
    }

    rebuilt = dict_to_tree(data)
    assert preorder(rebuilt) == preorder(root)

    # Test 5: Grafting
    dog_leaf = root.no_child

    graft_new_knowledge(
        dog_leaf,
        "Does it bark?",
        "Cat",
        False
    )

    assert dog_leaf.text == "Does it bark?"
    assert dog_leaf.yes_child.text == "Dog"
    assert dog_leaf.no_child.text == "Cat"

    # Test 6: New guess on YES
    eagle_leaf = root.yes_child

    graft_new_knowledge(
        eagle_leaf,
        "Is it a bird?",
        "Parrot",
        True
    )

    assert eagle_leaf.yes_child.text == "Parrot"
    assert eagle_leaf.no_child.text == "Eagle"

    # Test 7: Empty tree
    assert count_nodes(None) == 0
    assert count_leaves(None) == 0
    assert tree_height(None) == -1
    assert preorder(None) == []
    assert inorder(None) == []
    assert postorder(None) == []
    assert tree_to_dict(None) is None
    assert dict_to_tree(None) is None

    print("All 7 tests passed!")
    print("Score: 100/100")

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        engine = MindReaderEngine()
        engine.run()