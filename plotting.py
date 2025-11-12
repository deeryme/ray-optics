import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm

#%% Flat

max_delta_Y = 4     # mm
v_pts_per_mm = 16
heights = np.linspace(0,max_delta_Y,max_delta_Y*v_pts_per_mm+1)     

h_pts_per_mm = 16
max_delta_X = 2 # mm; mirror's tangential displacement
num_translations = 2*max_delta_X*h_pts_per_mm+1
x = np.linspace(-max_delta_X, max_delta_X, num_translations)
P = np.zeros((len(heights), len(x)))


with open("flat/heights.json", 'r') as f:
    h_file_names = json.load(f)

flat_data = {}
# ========== IMPORT DETECTOR DATA TO JSON ==========
for h, name in enumerate(h_file_names):
    data_path = f"flat/{name}/{name}.json"
    with open(data_path, 'r') as f:
        flat_data[name] = json.load(f)
    test = [flat_data[name][idx]['power'] for idx in range(len(flat_data[name]))]
    P[h,:] = test
    
P_min = np.min(P)
P = P/P_min

png_padding = 0.5
    
xx, hh = np.meshgrid(x, heights)

   
fig_3d = plt.figure()
ax_3d = fig_3d.add_subplot(111, projection='3d')
ax_3d.plot_surface(xx, hh, np.abs(P), cmap=cm.coolwarm)
ax_3d.set_xlabel("$x$ (mm)", fontsize='large')
ax_3d.set_ylabel("$h$ (mm)", fontsize='large')
ax_3d.set_zlabel("Relative Power", fontsize='large')
ax_3d.set_title("Power vs Displacement: $P(x,h)$\n" + r"(normalised by $P_{max}$ =" + f"{-P_min:02.2f} B/s)", fontsize='large')
plt.savefig("flat/flat_P_v_DX_DY.png", transparent=True, bbox_inches='tight', pad_inches=png_padding)


fig_ctr = plt.figure("Contour plot of P(x,h)")
plt.title("Power vs Displacement: $P(x,h)$", fontsize='large')
plt.contourf(xx, hh, P, cmap=cm.coolwarm)
plt.colorbar()
plt.grid(True)
plt.xlabel("$x$ (mm)", fontsize='large')
plt.ylabel("$h$ (mm)", fontsize='large')
plt.savefig("flat/flat_P_contour.png", transparent=True, bbox_inches='tight')



print("Showing Plot...")
plt.show()
print("Closing Viewer")

#%% Concave
mirror_h        = 4.0       # mm; indicates the height of the mirror endpts
mirror_w        = 1.0       # mm
r               = 2.525    # mm; radius of curvature <<<<<<<<
d               = 0.05     # mm <<<<<<<<<
is_concave_up   = False      # <<<<<<<<<

concavity = 'up' if is_concave_up else 'down'
max_delta_Y = 4     # mm
v_pts_per_mm = 8            # <<<<<<<<<
heights = np.linspace(0,max_delta_Y,max_delta_Y*v_pts_per_mm+1)   
tops = heights
if concavity == 'up':       # line up the tops
    heights[0] += d
elif concavity == 'down':
    heights[1:] -= d
tops[0] += d

h_pts_per_mm = v_pts_per_mm
max_delta_X = 2 # mm; mirror's tangential displacement
num_translations = 2*max_delta_X*h_pts_per_mm+1
x = np.linspace(-max_delta_X, max_delta_X, num_translations)
P = np.zeros((len(heights), len(x)))


# Concave (with radius r)
mir_r_str = 'f'.join(f"{r:.4f}".split('.'))
main_dir_name = f"concave_{concavity}_r_{mir_r_str}mm"
with open(f"{main_dir_name}/tops.json", 'r') as f:
    tops_names = json.load(f)
 

concave_data = {}
# ========== IMPORT DETECTOR DATA TO JSON ==========
for t, name in enumerate(tops_names):
    data_path = f"{main_dir_name}/{name}/{name}.json"
    with open(data_path, 'r') as f:
        concave_data[name] = json.load(f)
    horiz_sweep = [concave_data[name][idx]['power'] for idx in range(len(concave_data[name]))]
    P[t,:] = horiz_sweep
    
P_min = np.min(P)
P = P/P_min

png_padding = 0.5

xx, hh = np.meshgrid(x, tops)
   
fig_3d = plt.figure()
ax_3d = fig_3d.add_subplot(111, projection='3d')
ax_3d.plot_surface(xx, hh, np.abs(P), cmap=cm.coolwarm)
ax_3d.set_xlabel("$x$ (mm)", fontsize='large')
ax_3d.set_ylabel("$h$ (mm)", fontsize='large')
ax_3d.set_zlabel("Relative Power", fontsize='large')
ax_3d.set_title("Power vs Displacement: $P(x,h)$\n" + r"(normalised by $P_{max}$ =" + f"{-P_min:02.2f} B/s)", fontsize='large')
plt.savefig(f"{main_dir_name}/P_v_DX_DY.png", transparent=True, bbox_inches='tight', pad_inches=png_padding)


fig_ctr = plt.figure("Contour plot of P(x,h)")
plt.title("Power vs Displacement: $P(x,h)$", fontsize='large')
plt.contourf(xx, hh, P, cmap=cm.coolwarm)
plt.colorbar()
plt.grid(True)
plt.xlabel("$x$ (mm)", fontsize='large')
plt.ylabel("$h$ (mm)", fontsize='large')
plt.savefig(f"{main_dir_name}/P_contour.png", transparent=True, bbox_inches='tight')



print("Showing Plot...")
plt.show()
print("Closing Viewer")



