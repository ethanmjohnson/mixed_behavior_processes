def find_petri_net_diameter(file_path):

    """
    This function finds the diameter of a Petri net using the longest shortest paths.

    Inputs:
    file_path: the file path to the Petri net

    Outputs:
    diameter: the diameter of the Petri net
    """

    import networkx as nx
    import pm4py

    # read in the petri net path
    net, im, fm = pm4py.read_pnml(file_path)

    # initialise a directed graph
    G = nx.DiGraph()

    # add the places from the net as nodes to G
    for place in net.places:
        G.add_node(place.name, type="place")

    # add transitions from the net as nodes to G
    for transition in net.transitions:
        label = transition.label if transition.label else transition.name
        G.add_node(transition.name, type="transition", label=label)

    # add the arcs from the net as edges in G
    for arc in net.arcs:
        G.add_edge(arc.source.name, arc.target.name)

    # find the shortest path length between all nodes in G
    lengths = dict(nx.all_pairs_shortest_path_length(G))

    # find the longest shortest path
    diameter = 0
    for source in lengths:
        for target in lengths[source]:
            diameter = max(diameter, lengths[source][target])

    return diameter

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
        uncoordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_2.pnml")
        coordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_1.pnml")
    else:
        uncoordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_uncoordinated.pnml")
        coordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_coordinated.pnml")

    u_diameter = find_petri_net_diameter(uncoordinated_data)
    c_diameter = find_petri_net_diameter(coordinated_data)

    print("Diameter of", args.country, "(uncoordinated): ", u_diameter)
    print("Diameter of", args.country, "(coordinated): ", c_diameter)