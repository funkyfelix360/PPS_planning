import numpy as np
from time import time as timestamp, sleep

import matplotlib; matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

import dataloading as load
import PPSSimulation as pps
from PPSSimulation import sim_date


# import webapp as web

def build_dataset():
    """
    Loads and processes production orders and operation cycles data from SQL files.
    Creates ProductionOrder and OperationCycle objects and organizes them into collections.

    Returns:
        tuple: Contains:
            - production_orders (dict): Dictionary of ProductionOrder objects keyed by PA
            - opcs (list): List of all OperationCycle objects
            - workplaces (ndarray): Sorted array of unique workplace names
            - opcs_by_PA (dict): Dictionary of OperationCycle objects grouped by PA
    """
    print('Loading data')
    t0 = timestamp()

    # get POs as dataframe
    production_orders_data = load.get_sql_data('.\\load_PO_data.sql')
    # get opcs as dataframe
    opcs_data = load.get_sql_data('.\\load_opc_data.sql')

    workplaces_data = np.unique(opcs_data[["WorkPlaceName"]].to_numpy().flatten())
    workplaces = {}
    for workplace in workplaces_data:
        workplaces[workplace] = pps.Workplace(workplace)

    opcs = {}
    opcs_by_PA = {}
    # generate and group opcs by PA
    for _, row in opcs_data.iterrows():
        obj = pps.OperationCycle(*row)
        opcs[obj.opcID] = obj
        if row['PA'] not in opcs_by_PA:
            opcs_by_PA[row['PA']] = [obj]
        else:
            opcs_by_PA[row['PA']].append(obj)

    # generate all PA, reference opcs
    production_orders = {}
    for _, row in production_orders_data.iterrows():
        try:
            production_orders[row['PA']] = pps.ProductionOrder(row['PA'], opcs_by_PA[row['PA']])
        except KeyError as e:
            print(f'Could not find {row["PA"]} in opcs_by_PA')
            print(e)
            continue
        except Exception as e:
            print(f'Could not create ProductionOrder for {row["PA"]}')
            continue

    for pa in production_orders.keys():
        for opc in production_orders[pa].operationcycles:
            opc.next_step = production_orders[pa].operationcycles[production_orders[pa].operationcycles.index(opc)+1] if production_orders[pa].operationcycles.index(opc)+1 < len(production_orders[pa].operationcycles) else None

    for opc in opcs.values():
        try:
            opc.PA = production_orders[opc.PA]
        except KeyError as e:
            print(f'Could not find {opc.PA} in production_orders')
            print(e)
            continue

    print(f'Loading time elapsed: {timestamp() - t0}')

    # find active opc_id
    for pa in production_orders.keys():
        if production_orders[pa].FinishedDate: # skip all the finished PAs
            continue
        opcs_of_PA = opcs_by_PA[pa]
        for opc in reversed(opcs_of_PA): # go from the end of the list to prevent starting on a skipped opc
            if opc.opc_state!=0:
                production_orders[pa].current_step = opc
                break
        if production_orders[pa].current_step:
            if production_orders[pa].current_step.workplace:
                workplaces[production_orders[pa].current_step.workplace].input_wip.append(production_orders[pa])

    # TODO Add workplaces in OPC as Object

    return production_orders, opcs, workplaces, opcs_by_PA

if __name__ == '__main__':
    # start with getting the data set from sql
    production_orders, opcs, workplaces, opcs_by_PA = build_dataset()
    simtime = pps.sim_date()
    fig, ax = plt.subplots()
    names = [workplaces[wp].name for wp in workplaces.keys()]
    # creating the first plot and frame
    graph = ax.bar(names, [len(workplaces[wp].input_wip) for wp in workplaces.keys()])
    ax.set_xlabel("Workplace")
    ax.set_ylabel("WIP in PA")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right")

    # updates the data and graph
    def update(frame):
        global graph
        for wp in workplaces.values():
            wp.run(simtime)
        # first process all wps, then ship them. Else process A, shipping to B then processing B results in PAs jumping multiple times in a sim day
        for wp in workplaces.values():
            wp.ship_output_wip()
        # updating the graph
        heights = [len(workplaces[wp].input_wip) for wp in workplaces.keys()]
        for bar, h in zip(graph, heights):
            bar.set_height(h)
        simtime.next_day()
        print(f'Frame: {frame}', simtime.date)
        sleep(.5)
        return graph

global anim
anim = FuncAnimation(fig, update, frames=200)
plt.show()
