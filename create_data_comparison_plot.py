import dataloading as load
import plotting as plt
import pandas as pd

secret_path = 'P:/Public/Laufende_Projekte_kein_invest/2026 PPS Planung/Programmierung/data/'


if __name__ == '__main__':

    #days_offset = 14
    #dispatchlists = load.get_sql_data(secret_path + 'dispatch_data.sql', args={'days_offset': days_offset}).set_index('SnapshotDate').todict()
    dispatchlists = load.get_sql_data(secret_path + 'dispatch_data.sql', args={})
    dispatchlists["SnapshotDate"] = pd.to_datetime(dispatchlists["SnapshotDate"])
    print(dispatchlists)
    print(dispatchlists.stack())
    fig, ax = plt.initialize_simple_plot()

    for date in dates:
        entries = dispatchlists[dispatchlists['SnapshotDate'] == date]
        print(entries)
