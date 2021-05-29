import sys
from Trees.src.trees.bst_tree import BST
from Trees.src.donor_prog.donor import Donor
from Trees.src.errors import MissingValueError


def donor_runner() -> None:
    Donor.create_from_file(sys.argv[1])
    donor_tree: "BST" = BST()
    for instance in Donor.instances:
        donor_tree.add_value(instance.amount)
    if sys.argv[2] == 'all':
        while donor_tree:
            node = donor_tree.get_min_node()
            for instance in Donor.instances:
                if instance.amount == node.value:
                    print(instance)
            donor_tree.remove_value(node.value)
    elif sys.argv[2] == 'rich':
        rich = donor_tree.get_max_node()
        for instance in Donor.instances:
            if instance.amount == rich.value:
                print(instance)
    elif sys.argv[2] == 'cheap':
        cheap = donor_tree.get_min_node()
        for instance in Donor.instances:
            if instance.amount == cheap.value:
                print(instance)
    elif sys.argv[2] == 'who':
        if '+' in sys.argv[3]:
            value_plus = int(sys.argv[3])
            if value_plus < donor_tree.get_max_node().value:
                try:
                    donor_tree.get_node(value_plus)
                except MissingValueError:
                    pass
                finally:
                    donor_tree.add_value(value_plus)
                    donor = donor_tree.get_node(value_plus).parent
                    if donor is not None:
                        for instance in Donor.instances:
                            if instance.amount == donor.value:
                                print(instance)
                        donor_tree.remove_value(value_plus)
            else:
                print(f"No Match")
        elif '-' in sys.argv[3]:
            value_minus = abs(int(sys.argv[3]))
            if value_minus > donor_tree.get_min_node().value:
                try:
                    donor_tree.get_node(value_minus)
                except MissingValueError:
                    pass
                finally:
                    donor_tree.add_value(value_minus)
                    donor = donor_tree.get_node(value_minus).parent.parent.parent
                    if donor is not None:
                        for instance in Donor.instances:
                            if instance.amount == donor.value:
                                print(instance)
                        donor_tree.remove_value(value_minus)
            else:
                print(f"No Match")
        else:
            value = int(sys.argv[3])
            try:
                donor = donor_tree.get_node(value)
            except MissingValueError:
                print(f"No Match")
            else:
                for instance in Donor.instances:
                    if instance.amount == donor.value:
                        print(instance)


donor_runner()
