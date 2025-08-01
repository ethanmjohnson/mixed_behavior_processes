
def get_operators(tree):

    """
    This function finds the different gates within the process tree

    Inputs:
    tree: a process tree

    Outputs:
    operators: a list containing the different operators in the process tree
    """
    # initialise the list to contain the operators
    operators = []

    # Recursively traverses the tree starting from the given node.
    # For each node with a defined operator, appends the operator to the `operators` list
    # and continues the traversal on its children.
    def recurse(node):
        if node.operator is not None:
            operators.append(node.operator)
            for child in node.children:
                recurse(child)
    recurse(tree)
    return operators


def find_gate_count(file_path):
    """
    This function discovers a process tree from an event log and then finds the number of XOR and AND gates in this process tree.

    Inputs:
    file_path: the path to an event log

    Outputs:
    xor_count: the number of XOR gates in the discovered process tree
    and_count: the number of AND gates in the discovered process tree
    """
    from pm4py.algo.discovery.inductive import algorithm as inductive_miner
    from pm4py.objects.log.importer.xes.importer import apply as xes_importer

    # read in the event log
    log = xes_importer(file_path)

    # discover a process tree
    parameters = {
        "noise_threshold": 0.2 
    }

    tree = inductive_miner.apply(log, variant=inductive_miner.Variants.IMf, parameters=parameters)


    # find the operators in the process tree

    operators = get_operators(tree)

    # initialise the counts
    xor_count = 0
    and_count = 0

    # count the number of XOR (X) and AND (+) operators in the tree
    for operator in operators:
        operator = str(operator)
        if operator == "X":
            xor_count += 1
        if operator == "+":
            and_count += 1

    return xor_count, and_count

if __name__ == "__main__":
    from load_config import load_config
    import os
    import argparse

    config = load_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("--country", type=str, required=True, choices=["brazil", "uae", "spain", "honduras", "thailand", "thailand_split", "spain_split", "brazil_2_split"], help="Name of the country to calculate Petri net diameter for")
    args = parser.parse_args()

    # Construct dataset path

    if args.country == "brazil":
        uncoordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_2.xes")
        coordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_1.xes")
    else:
        uncoordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_uncoordinated.xes")
        coordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_coordinated.xes")

    u_xor_count, u_and_count = find_gate_count(uncoordinated_data)
    c_xor_count, c_and_count = find_gate_count(coordinated_data)

    print("Number of XOR gates in", args.country, "(uncoordinated):", u_xor_count)
    print("Number of AND gates in", args.country, "(uncoordinated): ", u_and_count)

    print("Number of XOR gates in", args.country, "(coordinated):", c_xor_count)
    print("Number of AND gates in", args.country, "(coordinated): ", c_and_count)
