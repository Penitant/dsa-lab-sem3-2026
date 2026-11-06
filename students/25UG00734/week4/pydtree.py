
class TreeNode:
 
    def __init__(self, text, yes_child=None, no_child=None):
        self.text = text.strip()
        self.yes_child = yes_child
        self.no_child = no_child

    def is_leaf(self):
        return self.yes_child is None and self.no_child is None

    def __repr__(self):
        if self.is_leaf():
            return "Leaf('" + self.text + "')"
        return "Decision('" + self.text + "')"


# =====================================================================
# Milestone 2: Tree Metrics
# =====================================================================


def count_nodes(root):
    """Total number of nodes."""
    if root is None:
        return 0
    return 1 + count_nodes(root.yes_child) + count_nodes(root.no_child)


def count_leaves(root):
    """Number of leaf nodes (final guesses)."""
    if root is None:
        return 0
    if root.is_leaf():
        return 1
    return count_leaves(root.yes_child) + count_leaves(root.no_child)


def tree_height(root):
    """Empty tree = -1, single node = 0, else 1 + max(child heights)."""
    if root is None:
        return -1
    return 1 + max(tree_height(root.yes_child), tree_height(root.no_child))


# =====================================================================
# Milestone 3: Tree Traversals
# =====================================================================


def preorder_traversal(root):
    """Root -> Yes -> No."""
    if root is None:
        return []
    return [root.text] + preorder_traversal(root.yes_child) + preorder_traversal(root.no_child)


def postorder_traversal(root):
    """Yes -> No -> Root."""
    if root is None:
        return []
    return postorder_traversal(root.yes_child) + postorder_traversal(root.no_child) + [root.text]


def inorder_traversal(root):
    """Yes -> Root -> No."""
    if root is None:
        return []
    return inorder_traversal(root.yes_child) + [root.text] + inorder_traversal(root.no_child)


# =====================================================================
# Milestone 6: Terminal ASCII Tree Visualizer
# =====================================================================


def _label(node):
    if node.is_leaf():
        return '[Guess]: "' + node.text + '"'
    return '[Question]: "' + node.text + '"'


def print_ascii_tree(root, prefix="", is_tail=True, choice=""):
    """Prints the tree as a branching diagram using plain ASCII."""
    if root is None:
        print("(empty tree)")
        return

    branch = "`-- " if is_tail else "|-- "
    tag = "(" + choice + ") " if choice else ""
    print(prefix + branch + tag + _label(root))

    children = []
    if root.yes_child:
        children.append(("Yes", root.yes_child))
    if root.no_child:
        children.append(("No", root.no_child))

    new_prefix = prefix + ("    " if is_tail else "|   ")
    for i in range(len(children)):
        c_choice, child = children[i]
        print_ascii_tree(child, new_prefix, i == len(children) - 1, c_choice)


# =====================================================================
# Milestone 4: Serialization (Save / Load)
# =====================================================================


def tree_to_dict(root):
    """Converts a tree into nested dictionaries."""
    if root is None:
        return None
    return {
        "text": root.text,
        "yes": tree_to_dict(root.yes_child),
        "no": tree_to_dict(root.no_child),
    }


def dict_to_tree(data):
    """Rebuilds a tree from nested dictionaries."""
    if data is None:
        return None
    return TreeNode(data["text"], dict_to_tree(data["yes"]), dict_to_tree(data["no"]))


def _tree_to_lines(root, lines):
    """Preorder dump: 'Q|text' for questions, 'L|text' for leaves."""
    if root.is_leaf():
        lines.append("L|" + root.text)
    else:
        lines.append("Q|" + root.text)
        _tree_to_lines(root.yes_child, lines)
        _tree_to_lines(root.no_child, lines)


def _build_from_lines(lines, pos):
    """Reads one subtree from lines, starting at pos[0]."""
    if pos[0] >= len(lines):
        raise ValueError("File ended too early.")
    line = lines[pos[0]]
    pos[0] += 1
    if line[:2] == "L|":
        return TreeNode(line[2:])
    if line[:2] == "Q|":
        yes_child = _build_from_lines(lines, pos)
        no_child = _build_from_lines(lines, pos)
        return TreeNode(line[2:], yes_child, no_child)
    raise ValueError("Bad line in file: " + line)


def save_tree_to_file(root, filename):
    """Saves the tree to a text file (one node per line, preorder)."""
    lines = []
    _tree_to_lines(root, lines)
    f = open(filename, "w", encoding="utf-8")
    f.write("\n".join(lines))
    f.close()


def load_tree_from_file(filename):
    """Loads a tree from a text file. Raises FileNotFoundError / ValueError."""
    f = open(filename, "r", encoding="utf-8")
    content = f.read()
    f.close()
    lines = content.split("\n")
    if lines == [""]:
        raise ValueError("File contains an empty tree structure.")
    return _build_from_lines(lines, [0])


# =====================================================================
# Milestone 5: Dynamic Pointer Mutation (Grafting New Knowledge)
# =====================================================================


def graft_new_knowledge(leaf_node, new_question, new_guess, new_guess_is_yes):
    """Turns an existing leaf into a question node, in place.

    Old leaf 'Dog', new item 'Cat', question 'Does it meow?', Cat -> Yes:
        node becomes Question('Does it meow?'), yes = Cat, no = Dog
    """
    old_guess = leaf_node.text
    new_leaf = TreeNode(new_guess)
    old_leaf = TreeNode(old_guess)

    leaf_node.text = new_question.strip()
    if new_guess_is_yes:
        leaf_node.yes_child = new_leaf
        leaf_node.no_child = old_leaf
    else:
        leaf_node.yes_child = old_leaf
        leaf_node.no_child = new_leaf


def create_default_seed_tree():
    """A small starter tree."""
    root = TreeNode("Does it live in water?")
    root.yes_child = TreeNode("Dolphin")

    land_branch = TreeNode("Does it bark?")
    land_branch.yes_child = TreeNode("Dog")
    land_branch.no_child = TreeNode("Elephant")

    root.no_child = land_branch
    return root


# =====================================================================
# Milestone 7: Unit Tests
# =====================================================================


def run_tests():
    print("=" * 60)
    print("Running PyDTree Milestone Verification Test Suite...")
    print("=" * 60)

    # Test 1
    n_leaf = TreeNode("Cheetah")
    assert n_leaf.is_leaf() is True, "Test 1 Failed: leaf"
    n_internal = TreeNode("Has stripes?", yes_child=n_leaf, no_child=TreeNode("Lion"))
    assert n_internal.is_leaf() is False, "Test 1 Failed: internal"
    print("  OK Test 1: Node & Leaf properties verified.")

    # Test 2
    assert count_nodes(None) == 0
    assert count_leaves(None) == 0
    assert tree_height(None) == -1
    assert tree_height(n_leaf) == 0
    assert count_leaves(n_leaf) == 1
    print("  OK Test 2: Edge cases (None, single node) verified.")

    # Test 3
    assert count_nodes(n_internal) == 3
    assert count_leaves(n_internal) == 2
    assert tree_height(n_internal) == 1
    print("  OK Test 3: Metrics on multi-level tree verified.")

    # Test 4
    assert preorder_traversal(n_internal) == ["Has stripes?", "Cheetah", "Lion"]
    assert postorder_traversal(n_internal) == ["Cheetah", "Lion", "Has stripes?"]
    assert inorder_traversal(n_internal) == ["Cheetah", "Has stripes?", "Lion"]
    print("  OK Test 4: Pre-order, In-order, Post-order verified.")

    # Test 5
    lion_leaf = n_internal.no_child
    graft_new_knowledge(lion_leaf, "Does it have a mane?", "Lioness", False)
    assert not lion_leaf.is_leaf()
    assert lion_leaf.text == "Does it have a mane?"
    assert lion_leaf.yes_child.text == "Lion"
    assert lion_leaf.no_child.text == "Lioness"
    assert tree_height(n_internal) == 2
    assert count_leaves(n_internal) == 3
    print("  OK Test 5: Knowledge grafting verified.")

    # Test 6
    reconstructed = dict_to_tree(tree_to_dict(n_internal))
    assert count_nodes(reconstructed) == count_nodes(n_internal)
    assert preorder_traversal(reconstructed) == preorder_traversal(n_internal)
    print("  OK Test 6: Dictionary round-trip verified.")

    # Test 7
    seed = create_default_seed_tree()
    assert count_nodes(seed) == 5
    assert count_leaves(seed) == 3
    assert tree_height(seed) == 2
    print("  OK Test 7: Default seed tree verified.")

    print("\n" + "=" * 60)
    print("ALL 7 TESTS PASSED!")
    print("=" * 60)


# =====================================================================
# Milestone 6: Interactive Game Engine
# =====================================================================


class MindReaderEngine:
    def __init__(self, seed_file=None):
        self.knowledge_file = seed_file or "dtree_knowledge.txt"
        try:
            self.root = load_tree_from_file(self.knowledge_file)
            print("[*] Loaded existing knowledge base from '" + self.knowledge_file + "'.")
        except (FileNotFoundError, ValueError):
            self.root = create_default_seed_tree()
            print("[*] Initialized fresh default knowledge seed tree.")

    def ask_yes_no(self, prompt):
        while True:
            ans = input(prompt + " (yes/no): ").strip().lower()
            if ans in ("y", "yes"):
                return True
            if ans in ("n", "no"):
                return False
            print("Please enter 'yes' or 'no'.")

    def play_round(self):
        print("\n" + "-" * 50)
        print("Think of any animal, character, or everyday object.")
        print("I will try to guess it by asking Yes/No questions!")
        print("-" * 50)
        input("Press [Enter] when you are ready...")

        curr = self.root
        while not curr.is_leaf():
            if self.ask_yes_no(curr.text):
                curr = curr.yes_child
            else:
                curr = curr.no_child

        print("\nMy guess is: Is it a " + curr.text + "?")
        if self.ask_yes_no("Did I get it right?"):
            print("\nYay! Binary decision trees win again!")
            return

        print("\nDrat! You outsmarted my current knowledge base.")
        new_item = input("What were you actually thinking of? > ").strip()
        if new_item == "":
            print("No answer provided. Skipping learning step.")
            return

        old_guess = curr.text
        dist_question = input(
            "Give me a Yes/No question that distinguishes a '"
            + new_item
            + "' from a '"
            + old_guess
            + "':\n> "
        ).strip()
        if not dist_question.endswith("?"):
            dist_question += "?"

        ans_for_new = self.ask_yes_no("For a '" + new_item + "', what is the correct answer?")

        graft_new_knowledge(curr, dist_question, new_item, ans_for_new)
        print("\nBrain updated! I have added '" + new_item + "' to my tree.")

        try:
            save_tree_to_file(self.root, self.knowledge_file)
            print("[OK] Saved updated tree to '" + self.knowledge_file + "'.")
        except Exception as e:
            print("[!] Warning: Could not save knowledge file: " + str(e))

    def start_repl(self):
        print("=" * 60)
        print("  MindReader 2000 - Adaptive Knowledge Tree Engine")
        print("=" * 60)

        while True:
            print("\n[Menu Options]:")
            print("  1. Play 20-Questions (Teach the tree)")
            print("  2. Display Visual Tree")
            print("  3. View Tree Statistics (Height, Leaves, Nodes)")
            print("  4. View Traversals (Pre-order, In-order, Post-order)")
            print("  5. Reset to Default Seed Tree")
            print("  6. Exit")
            print("  7. Run Unit Tests")

            choice = input("\nEnter choice [1-7]: ").strip()
            if choice == "1":
                self.play_round()
            elif choice == "2":
                print("\nCurrent Knowledge Tree:")
                print_ascii_tree(self.root)
            elif choice == "3":
                print("\nTree Statistics:")
                print("  Total Nodes:  " + str(count_nodes(self.root)))
                print("  Total Leaves: " + str(count_leaves(self.root)))
                print("  Tree Height:  " + str(tree_height(self.root)) + " edges")
            elif choice == "4":
                print("\nTree Walks:")
                print("  Pre-order:  " + str(preorder_traversal(self.root)))
                print("  In-order:   " + str(inorder_traversal(self.root)))
                print("  Post-order: " + str(postorder_traversal(self.root)))
            elif choice == "5":
                if self.ask_yes_no("Are you sure you want to reset knowledge to default?"):
                    self.root = create_default_seed_tree()
                    save_tree_to_file(self.root, self.knowledge_file)
                    print("[OK] Knowledge base reset.")
            elif choice == "6" or choice.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break
            elif choice == "7":
                run_tests()
            else:
                print("Invalid selection. Please choose a number between 1 and 7.")


if __name__ == "__main__":
    engine = MindReaderEngine()
    engine.start_repl()