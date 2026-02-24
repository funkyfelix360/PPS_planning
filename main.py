import pandas as pd

import dataloading as load

# I first want to generate all the necessary workplaces and dispatchlists

# get POs as dataframe
with open('load_PO_data.sql.sql', 'r') as file:
    production_orders = load.get_sql_data(file.read())

# get opcs as dataframe
with open('load_opc_data.sql', 'r') as file:
    opcs = load.get_sql_data(file.read())

dipatchdepartments = production_orders["Dispatchdepartment"].to_numpy()
workplaces = production_orders["WorkplaceName"].to_numpy()

