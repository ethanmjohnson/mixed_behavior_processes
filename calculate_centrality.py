def calculate_centrality(file_path):

    import pm4py
    import networkx as nx
    from pm4py.objects.petri_net.utils.networkx_graph import create_networkx_directed_graph

    net, im, fm = pm4py.read_pnml(file_path)

    G, id = create_networkx_directed_graph(net)
    cc = nx.closeness_centrality(G)

    eigen = nx.eigenvector_centrality(G, max_iter=1000)
    between = nx.betweenness_centrality(G)
    average_cc = sum(cc.values())/len(cc)
    average_between = sum(between.values())/len(between)
    average_eigen = sum(eigen.values())/len(eigen)

    return average_cc, average_between, average_eigen



if __name__ == "__main__":
    from load_config import load_config
    import os
    import argparse

    config = load_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("--country", type=str, required=True, choices=["brazil", "uae", "spain", "honduras", "thailand", "thailand_split", "spain_split", "brazil_2_split"], help="Name of the country to calculate Petri net diameter for")
    args = parser.parse_args()

    if args.country == "brazil":
        uncoordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_2.pnml")
        coordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_1.pnml")
    else:
        uncoordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_uncoordinated.pnml")
        coordinated_data = os.path.join(config["project_root"], "data", args.country.lower() + "_coordinated.pnml")

    average_cc_c, average_between_c, average_eigen_c = calculate_centrality(coordinated_data)
    average_cc_u, average_between_u, average_eigen_u = calculate_centrality(uncoordinated_data)


    print("Average closeness centrality of", args.country, "(coordinated):", average_cc_c)
    print("Average betweenness centrality of", args.country, "(coordinated):", average_between_c)
    print("Average eigenvector centrality of", args.country, "(coordinated):", average_eigen_c)

    print("Average closeness centrality of", args.country, "(uncoordinated):", average_cc_u)
    print("Average betweenness centrality of", args.country, "(uncoordinated):", average_between_u)
    print("Average eigenvector centrality of", args.country, "(uncoordinated):", average_eigen_u)
