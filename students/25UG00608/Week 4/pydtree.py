
"""
Week 4 - Trees
Animal Guessing Game using a Binary Decision Tree

Run tests:
    python pydtree.py --test

Run game:
    python pydtree.py
"""

import json
import sys


class TreeNode:
    def __init__(self, question, yes=None, no=None, animal=None):
        self.question = question
        self.yes = yes
        self.no = no
        self.animal = animal

    @property
    def is_leaf(self):
        return self.yes is None and self.no is None

    def count_nodes(self):
        return (
            1
            + (self.yes.count_nodes() if self.yes else 0)
            + (self.no.count_nodes() if self.no else 0)
        )

    def count_leaves(self):
        if self.is_leaf:
            return 1
        return (
            (self.yes.count_leaves() if self.yes else 0)
            + (self.no.count_leaves() if self.no else 0)
        )

    def height(self):
        if self.is_leaf:
            return 1
        return 1 + max(
            self.yes.height() if self.yes else 0,
            self.no.height() if self.no else 0
        )

    def preorder(self):
        result = [self.question]
        if self.yes:
            result.extend(self.yes.preorder())
        if self.no:
            result.extend(self.no.preorder())
        return result

    def inorder(self):
        result = []
        if self.yes:
            result.extend(self.yes.inorder())
        result.append(self.question)
        if self.no:
            result.extend(self.no.inorder())
        return result

    def postorder(self):
        result = []
        if self.yes:
            result.extend(self.yes.postorder())
        if self.no:
            result.extend(self.no.postorder())
        result.append(self.question)
        return result

    def to_dict(self):
        return {
            "question": self.question,
            "animal": self.animal,
            "yes": self.yes.to_dict() if self.yes else None,
            "no": self.no.to_dict() if self.no else None
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None

        node = cls(
            question=data["question"],
            animal=data.get("animal")
        )
        node.yes = cls.from_dict(data.get("yes"))
        node.no = cls.from_dict(data.get("no"))
        return node

    def to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def from_json(cls, filename):
        with open(filename, "r", encoding="utf-8") as file:
            return cls.from_dict(json.load(file))

    def visualize(self, prefix="", branch="ROOT"):
        label = self.animal if self.is_leaf else self.question
        lines = [prefix + branch + ": " + str(label)]

        if self.yes:
            lines.extend(
                self.yes.visualize(prefix + "    ", "YES").splitlines()
            )
        if self.no:
            lines.extend(
                self.no.visualize(prefix + "    ", "NO").splitlines()
            )

        return "\n".join(lines)

    def graft(self, new_animal, new_question, answer):
        """
        Replace the current leaf with a question node.
        The supplied answer determines which branch contains
        the old animal.
        """
        if not self.is_leaf:
            raise ValueError("Knowledge can only be grafted onto a leaf.")

        old_animal = self.animal or self.question
        new_leaf = TreeNode(new_animal, animal=new_animal)
        old_leaf = TreeNode(old_animal, animal=old_animal)

        self.question = new_question
        self.animal = None

        if answer:
            self.yes = new_leaf
            self.no = old_leaf
        else:
            self.yes = old_leaf
            self.no = new_leaf


def default_tree():
    """Create the initial animal guessing tree."""

    return TreeNode(
        "Does it live in water?",
        yes=TreeNode(
            "Does it have gills?",
            yes=TreeNode("Fish", animal="Fish"),
            no=TreeNode("Dolphin", animal="Dolphin")
        ),
        no=TreeNode(
            "Can it fly?",
            yes=TreeNode("Eagle", animal="Eagle"),
            no=TreeNode(
                "Is it a pet?",
                yes=TreeNode("Dog", animal="Dog"),
                no=TreeNode("Lion", animal="Lion")
            )
        )
    )


class MindReaderEngine:
    def __init__(self, root=None):
        self.root = root if root is not None else default_tree()

    def play(self):
        print("\nThink of an animal. I will try to guess it!")

        current = self.root

        while not current.is_leaf:
            answer = input(current.question + " (yes/no): ").strip().lower()

            while answer not in ("yes", "no", "y", "n"):
                answer = input("Please enter yes or no: ").strip().lower()

            if answer in ("yes", "y"):
                current = current.yes
            else:
                current = current.no

        answer = input(
            "Is your animal " + str(current.animal or current.question)
            + "? (yes/no): "
        ).strip().lower()

        if answer in ("yes", "y"):
            print("Great! I guessed it!")
        else:
            self.learn(current)

    def learn(self, current):
        old_animal = current.animal or current.question

        new_animal = input("What animal were you thinking of? ").strip()
        if not new_animal:
            print("Animal name cannot be empty.")
            return

        question = input(
            "Give me a question that distinguishes "
            + new_animal + " from " + str(old_animal) + ": "
        ).strip()

        if not question:
            print("Question cannot be empty.")
            return

        answer = input(
            "For " + new_animal + ", what is the answer? (yes/no): "
        ).strip().lower()

        while answer not in ("yes", "no", "y", "n"):
            answer = input("Please enter yes or no: ").strip().lower()

        current.graft(
            new_animal,
            question,
            answer in ("yes", "y")
        )

        print("Thank you! I have learned a new animal.")

    def run(self):
        while True:
            self.play()
            again = input("\nPlay again? (yes/no): ").strip().lower()
            if again not in ("yes", "y"):
                break

    def save(self, filename="animals.json"):
        self.root.to_json(filename)

    def load(self, filename="animals.json"):
        self.root = TreeNode.from_json(filename)


def run_tests():
    """Run basic tests for the tree implementation."""

    root = default_tree()

    assert root.count_nodes() == 11
    assert root.count_leaves() == 6
    assert root.height() == 4

    assert root.preorder()[0] == "Does it live in water?"
    assert root.inorder()
    assert root.postorder()[-1] == "Does it live in water?"

    data = root.to_dict()
    restored = TreeNode.from_dict(data)

    assert restored.count_nodes() == root.count_nodes()
    assert restored.count_leaves() == root.count_leaves()

    leaf = TreeNode("Cat", animal="Cat")
    leaf.graft("Rabbit", "Does it have long ears?", True)

    assert not leaf.is_leaf
    assert leaf.yes.animal == "Rabbit"
    assert leaf.no.animal == "Cat"

    print("All tests passed successfully!")


def main():
    if "--test" in sys.argv:
        run_tests()
        return

    engine = MindReaderEngine()

    try:
        engine.load()
        print("Previous animal knowledge loaded.")
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
        print("Starting with default animal knowledge.")

    print("\n===== ANIMAL MIND READER =====")
    print("1. Play game")
    print("2. Display tree")
    print("3. Display tree statistics")
    print("4. Save knowledge")
    print("5. Exit")

    while True:
        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            engine.run()

        elif choice == "2":
            print("\n" + engine.root.visualize())

        elif choice == "3":
            print("Total nodes:", engine.root.count_nodes())
            print("Leaf nodes:", engine.root.count_leaves())
            print("Tree height:", engine.root.height())
            print("Preorder:", engine.root.preorder())
            print("Inorder:", engine.root.inorder())
            print("Postorder:", engine.root.postorder())

        elif choice == "4":
            engine.save()
            print("Knowledge saved successfully.")

        elif choice == "5":
            engine.save()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1 to 5.")


if __name__ == "__main__":
    main()
    
