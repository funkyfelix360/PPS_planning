import numpy as np
import pandas as pd

import dataloading as load
import PPSSimulation as pps

# I first want to generate all the necessary workplaces and dispatchlists

# get POs as dataframe
production_orders_data = load.get_sql_data('.\\load_PO_data.sql')
production_orders = {}
# get opcs as dataframe
opcs_data = load.get_sql_data('.\\load_opc_data.sql')

dipatchdepartments = np.unique(opcs_data[["Dispatchdepartment"]].to_numpy().flatten()).sort()
workplaces = np.unique(opcs_data[["WorkPlaceName"]].to_numpy().flatten()).sort()

for _, row in production_orders.iterrows():
    paNumber = row['PA']
    opc_ids = opcs_data[opcs_data['PA'] == paNumber]
    production_orders[paNumber] = pps.ProductionOrder(paNumber, opc_ids)

