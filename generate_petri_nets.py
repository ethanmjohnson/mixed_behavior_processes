# this file generates a petri net from the event logs

def discover_petri_nets(file_path):
    """
    Discovers a Petri net using the inductive miner and saves to a .pnml file in the same folder as the event log is located.

    Inputs:
    file_path: path to an event log 
    """
    import pm4py
    print("loading event log...")
    log = pm4py.read_xes(file_path)
    print("discovering Petri net...")
    net, im, fm = pm4py.discover_petri_net_inductive(log, noise_threshold=0.2, multi_processing=True)

    return net, im, fm


if __name__ == "__main__":
    from load_config import load_config
    import os
    import argparse
    import pm4py

    config = load_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("--country", type=str, required=True, choices=["uae", "honduras", "brazil_1", "brazil_2", "thailand", "spain", "thailand_split", "spain_split", "brazil_2_split"], help="Name of the country to load event logs for")
    args = parser.parse_args()

    # Construct dataset path
    uncoordinated_path = os.path.join(config["project_root"], "data", args.country + "_uncoordinated.xes")
    coordinated_path = os.path.join(config["project_root"], "data", args.country + "_coordinated.xes")

    # construct output paths
    u_output_path = os.path.join(config["project_root"], "data", args.country + "_uncoordinated.pnml")
    c_output_path = os.path.join(config["project_root"], "data", args.country + "_coordinated.pnml")

    # discover petri net
    net_u, im_u, fm_u = discover_petri_nets(uncoordinated_path)
    net_c, im_c, fm_c = discover_petri_nets(coordinated_path)

    # save petri net
    pm4py.write_pnml(net_u, im_u, fm_u, u_output_path)
    pm4py.write_pnml(net_c, im_c, fm_c, c_output_path)
