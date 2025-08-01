def find_petri_net_density(file_path):
    """
    This function finds the density of a given petri net using the density for a directed graph.

    Inputs:
    file_path: the path to a Petri net

    Outputs:
    density: the density as a float
    """

    import pm4py

    net, im, fm = pm4py.read_pnml(file_path)

    # calculate the total number of nodes
    no_nodes = len(net.transitions) + len(net.places)

    # calculate the number of edges
    no_edges = len(net.arcs)

    # calculate the density using the density of a directed graph
    density = no_edges/(no_nodes*(no_nodes - 1))

    return density, no_nodes

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

    u_density, u_no_nodes = find_petri_net_density(uncoordinated_data)
    c_density, c_no_nodes = find_petri_net_density(coordinated_data)

    print("Number of nodes of", args.country, "(uncoordinated):", u_no_nodes)
    print("Density of", args.country, "(uncoordinated): ", u_density)
    print("Number of nodes of", args.country, "(coordinated):", c_no_nodes)
    print("Density of", args.country, "(coordinated): ", c_density)
