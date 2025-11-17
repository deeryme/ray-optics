import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm

def load_json_power_data(main_dir_name, P):
    with open(f"{main_dir_name}/tops.json", 'r') as f:
        tops_names = json.load(f)
    data = {}
    for top_level, name in enumerate(tops_names):
        data_path = f"{main_dir_name}/{name}/{name}.json"
        with open(data_path, 'r') as f:
            data[name] = json.load(f)
        horiz_sweep_P = [data[name][idx]['power'] for idx in range(len(data[name]))]
        P[top_level,:] = horiz_sweep_P
    return data

def plot_power_v_displacement(x, y, P, main_dir_name):
    P_min = np.min(P)
    P = P/P_min         # Plot abs. val. of power
    xx, yy = np.meshgrid(x, y)

    # 3D Plot
    png_padding = 0.5
    c_map = cm.inferno
    fig_3d = plt.figure("Surface plot of P(x,h)")
    ax_3d = fig_3d.add_subplot(111, projection='3d')
    ax_3d.plot_surface(xx, yy, np.abs(P), cmap=c_map, rstride=1, cstride=1)
    ax_3d.set_xlabel("$x$ (mm)", fontsize='large')
    ax_3d.set_ylabel("$h$ (mm)", fontsize='large')
    ax_3d.set_zlabel("Relative Power", fontsize='large')
    ax_3d.set_title("Power vs Displacement: $P(x,h)$\n" + r"(normalised by $P_{max}$ =" + f"{-P_min:02.2f} B/s)", fontsize='large')
    plt.savefig(f"{main_dir_name}/P_v_DX_DY.png", transparent=True, bbox_inches='tight', pad_inches=png_padding)

    # Contour Plot
    fig_ctr = plt.figure("Contour plot of P(x,h)")
    plt.title("Power vs Displacement: $P(x,h)$", fontsize='large')
    cbar_lvls = np.arange(0,1+0.01,0.01)
    plt.contourf(xx, yy, P, cmap=c_map, levels=cbar_lvls)
    cbar_ticks = cbar_lvls[::10]
    plt.colorbar(ticks=cbar_ticks)
    # CS = plt.contour(xx, yy, P, colors='white', linewidths=0.25, levels=cbar_ticks[1::2])
    # plt.clabel(CS, inline=True, fontsize=10)
    plt.grid(True)
    plt.xlabel("$x$ (mm)", fontsize='large')
    plt.ylabel("$h$ (mm)", fontsize='large')
    plt.savefig(f"{main_dir_name}/P_contour.png", transparent=True, bbox_inches='tight')

    # Uncomment to show interactive plot
    # print("Showing Plot...")
    # plt.show()
    # print("Closing Viewer")

def get_flat_mirr_plots():
    max_delta_Y = 4     # mm
    v_pts_per_mm = 16
    heights = np.linspace(0,max_delta_Y,max_delta_Y*v_pts_per_mm+1)     

    h_pts_per_mm = v_pts_per_mm
    max_delta_X = 2 # mm; mirror's lateral displacement
    num_translations = 2*max_delta_X*h_pts_per_mm+1
    x = np.linspace(-max_delta_X, max_delta_X, num_translations)
    P = np.zeros((len(heights), len(x)))

    main_dir_name = "../results/flat"
    # main_dir_name = "flat"
    load_json_power_data(main_dir_name, P)    
    plot_power_v_displacement(x, heights, P, main_dir_name)

def get_arc_mirr_plots(mirr_w, r, d, is_concave_up):
    concavity = 'up' if is_concave_up else 'down'
    max_delta_Y = 4     # mm
    v_pts_per_mm = 16          # <<<<<<<<<
    tops = np.linspace(0,max_delta_Y,max_delta_Y*v_pts_per_mm+1)
    # When exporting a JSON Scene, we'll take "top" to be the height of 
    # the highest part of the reflector  
    if concavity == 'up':       # line up the tops
        first_idx_gt_d = np.argmax(tops > d)
        tops = tops[first_idx_gt_d-1:]  # The top of a convex mirror can't go lower than d
        tops[0] = d
    elif concavity == 'down':
        last_idx_lt_d = np.where(tops < d)[0][-1] # np.where() ret obj is a bit weird
        tops = tops[last_idx_lt_d:]
        tops[0] = d



    h_pts_per_mm = v_pts_per_mm
    max_delta_X = 2 # mm; mirror's tangential displacement
    num_translations = 2*max_delta_X*h_pts_per_mm+1
    x = np.linspace(-max_delta_X, max_delta_X, num_translations)
    P = np.zeros((len(tops), len(x)))
    
    mir_r_str = 'f'.join(f"{r:.4f}".split('.'))
    main_dir_name = f"../mp_results/arc/concave_{concavity}_r_{mir_r_str}mm"
    load_json_power_data(main_dir_name, P)    
    plot_power_v_displacement(x, tops, P, main_dir_name)

if __name__ == "__main__":
    # UNCOMMENT THE DESIRED PLOT
    get_flat_mirr_plots()
    # get_arc_mirr_plots(1.0, 2.525, 0.05, True)
    # get_arc_mirr_plots(1.0, 2.525, 0.05, False)
    # get_arc_mirr_plots(1.0, 1.3, 0.1, True)
    # get_arc_mirr_plots(1.0, 1.3, 0.1, False)
    # get_arc_mirr_plots(1.0, 0.668, 0.22503, True)
    # get_arc_mirr_plots(1.0, 0.668, 0.22503, False)
    # add sim_result_locns & v_pts_per_mm args