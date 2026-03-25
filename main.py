import os
from time import sleep
from datetime import datetime
import matplotlib; matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import PPSSimulation as pps
import dataloading as load
secret_path = 'P:/Public/Laufende_Projekte_kein_invest/2026 PPS Planung/Programmierung/data/'

# import webapp as web

if __name__ == '__main__':
    # start with getting the data set from sql
    days_offset = 14
    for directory in ['./data', './logs', './plots']:
        os.makedirs(directory, exist_ok=True)
    production_orders, opcs, workplaces, dispatchdepartments, opcs_by_PA = pps.build_dataset(days_offset=days_offset,
                                                                                             # opcs_data=load.get_data(secret_path + 'opcs.csv'),
                                                                                             # production_orders_data=load.get_data(secret_path + 'production_orders.csv'),
                                                                                             mute=False)
    pps.day_based_simulation(production_orders, opcs, workplaces, dispatchdepartments, days_offset=days_offset)
