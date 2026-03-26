from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white"
})

def plotting_barpots(ax, ax2, x1, y1, x2, y2):
    # first try to remove all containers/content of plots, then redraw them
    ax.cla()
    ax.set_anchor((0,1))
    bp = ax.bar(x1, y1)
    ax.set_xticklabels([str(elem) for elem in x1], rotation=25, ha='right')
    ax.bar_label(bp, labels=[str(elem) for elem in y1], label_type='center')
    ax.set_xlabel("Dispatch Department")
    ax.set_ylabel("WIP in PA")
    ax.set_ylim(0, 150)
    ax.grid(linestyle = '--', linewidth = 0.5)

    ax2.cla()
    ax2.set_anchor((1,1))
    ax2.bar(x2, y2)

def initialize_plot(dispatchdepartments, workplaces, sim_date):
    """

    :param dispatchdepartments:
    :param workplaces:
    :return:
    """
    fig = plt.figure()
    gs = GridSpec(3, 10, figure=fig)
    ax = fig.add_subplot(gs[0:2, 0:8])
    ax.set_anchor((0,1))
    ax2 = fig.add_subplot(gs[0:2, 8:])
    ax2.set_anchor((1,1))
    ax_table = fig.add_subplot(gs[2, :])
    ax_table.set_anchor((0.5,1))
    # maximize window
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")

    names = [dispatchdepartments[disp].name for disp in dispatchdepartments.keys()]
    heights = [sum(len(workplaces[wp.name].input_wip) for wp in dispatchdepartments[disp].workplaces) for disp in
               dispatchdepartments.keys()]

    plotting_barpots(ax, ax2, names, heights, ['fertig'], [len(workplaces[wp].output_wip) for wp in workplaces.keys() if wp == 'Abschlussbuchung'])
    sats = plot_saturation(dispatchdepartments, {}, sim_date, fig, ax_table)
    plt.savefig('./plots/start.png')
    return fig, ax , ax2, ax_table, sats

def update_plot(fig, ax, ax2, ax_table, dispatchdepartments, workplaces, saturations, simtime, title='', filename=''):
    names = [dispatchdepartments[disp].name for disp in dispatchdepartments.keys()]
    heights = [sum(len(workplaces[wp.name].input_wip) for wp in dispatchdepartments[disp].workplaces) for disp in dispatchdepartments.keys()]
    plotting_barpots(ax, ax2, names, heights, ['fertig'],[len(workplaces['Abschlussbuchung'].output_wip)])

    saturations = plot_saturation(dispatchdepartments, saturations, simtime, fig, ax_table)

    fig.subplots_adjust(hspace=0.4, wspace=0.2, left=0.05, right=0.95, top=0.95, bottom=0.05)
    fig.suptitle(title)
    plt.draw()
    plt.pause(0.001)
    fig.savefig(filename)
    return saturations

def save_plot(fig, filename):
    fig.savefig(filename)
    plt.close(fig)

def plot_saturation(dispatchdepartments, sats, simtime, fig_table, ax_table):
    """

    :param dispatchdepartments:
    :param simtime:
    :return:
    """
    def get_color(a):
        if a < 20:
            return 'y'
        elif a > 150:
            return 'r'
        else:
            return 'w'

    ax_table.cla()
    ax_table.set_anchor((0.5,0))
    disps = ['Laser', 'Bohren & Fräsen', 'AOI', 'Dünnschichtlabor', 'Gal Cu Yasmin', 'Endprüfung Visuell']
    sat_of_day = []
    for disp in disps:
         sat_of_day.append(round(sum([len(wp.input_wip)/wp.capa_per_day * 100 for wp in dispatchdepartments[disp].workplaces]),1))
    # print('sats', sats, type(sats))
    sats[simtime.copy()] = sat_of_day
    # cellcolours = [['w']*len(disps)]*len([_ for _ in sats.keys()])

    cellcolours = [[get_color(sat) for sat in sat_of_day] for sat_of_day in sats.values()]
    # fig_table.patch.set_visible(False)
    ax_table.table(cellText=[sats[key] for key in sats.keys()], rowLabels=[key.string() for key in sats.keys()], colLabels=disps,
                   loc='upper center', cellColours=cellcolours)
    ax_table.axis('off')
    ax_table.axis('tight')
    return sats