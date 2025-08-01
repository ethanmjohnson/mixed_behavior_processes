

def log_split(log, net):

    '''
    This function splits an event log into its coordinated and uncoordinated components by removing any flower patterns

    Inputs:
    log: the event log to split into coordinated and uncoordinated components
    net: the petri net discovered from the event log to split

    Outputs:
    c_log: the event log corresponding to the coordinated component of log
    u_log: the event log corresponding to the uncoordinated component of log
    '''
    
    from pm4py.objects.log.obj import EventLog
    

    # initialise split logs

    c_log = EventLog()
    u_log = EventLog()

    # find the transition that begins the loop in the petri net

    loop_t = [t for t in net.transitions if 'init_loop_' in t.name]

    # find the place immediately after the loop transition

    loop_place = [arc.target for arc in net.arcs if arc.source in loop_t]

    # code to only choose loops that constitute a flower

    flower_places = []

    for p in loop_place:
        count = 0
        for arc in net.arcs:
            if arc.source == p and arc.target.label is not None:
                count+=1
        if count >=20:
            flower_places.append(p)

    # find all transitions that occur after this loop place

    flower_users = [arc.target.label for arc in net.arcs if arc.source in flower_places and arc.target.label is not None]

    # remove all traces that contain any if the flower users
    for trace in log:
        if any(event['concept:name'] in flower_users for event in trace):
            c_log.append(trace)
        else:
            u_log.append(trace)

    

    return c_log, u_log


if __name__ == "__main__":
    import pm4py

    from load_config import load_config
    import os
    import argparse
    from pm4py.objects.log.importer.xes import importer as xes_importer

    config = load_config()

    parser = argparse.ArgumentParser()
    parser.add_argument("--country", type=str, required=True, choices=["brazil", "uae", "spain", "honduras", "thailand"], help="Name of the country to split mixed behaviors from")
    args = parser.parse_args()

    if args.country == "brazil":
        log_path = os.path.join(config["project_root"], "data", args.country.lower() + "_2.xes")
        pn_path = os.path.join(config["project_root"], "data", args.country.lower() + "_2.pnml")
    else:
        log_path = os.path.join(config["project_root"], "data", args.country.lower() + "_uncoordinated.xes")
        pn_path = os.path.join(config["project_root"], "data", args.country.lower() + "_uncoordinated.pnml")

    
    # load petri net and event log

    
    variant = xes_importer.Variants.ITERPARSE
    parameters = {variant.value.Parameters.TIMESTAMP_SORT: True}
    log = xes_importer.apply(log_path, variant=variant, parameters=parameters)

    net, im, fm = pm4py.read_pnml(pn_path)


    c_log, u_log = log_split(log, net)

    print('discover uncoordinated petri net...')
    u_net, u_im, u_fm = pm4py.discover_petri_net_inductive(u_log, noise_threshold=0.2)
    print('discover coordinated petri net...')
    c_net, c_im, c_fm = pm4py.discover_petri_net_inductive(c_log, noise_threshold=0.2)


    pm4py.write_xes(u_log, os.path.join(config["project_root"], "data", args.country.lower() + "_split_uncoordinated.xes"))
    pm4py.write_xes(c_log, os.path.join(config["project_root"], "data", args.country.lower() + "_split_coordinated.xes"))
    pm4py.write_pnml(u_net, u_im, u_fm, os.path.join(config["project_root"], "data", args.country.lower() + "_split_uncoordinated.pnml"))
    pm4py.write_pnml(c_net, c_im, c_fm, os.path.join(config["project_root"], "data", args.country.lower() + "_split_coordinated.pnml"))

