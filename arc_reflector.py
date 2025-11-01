#!/usr/bin/env python3
"""
Ray Optics Simulation of tangential translation of reflector above photodetector
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sim_helper_functions import run_sim_startup_checks, create_gif_from_images, simulate_scene
import arc_scene as my_scene
import json
import copy


run_sim_startup_checks()
scene = copy.deepcopy(my_scene.SCENE)
mirror_h        = 4.0     # mm; indicates the height of the mirror endpts
mirror_w        = 1.0     # mm
r               = 0.5     # mm; radius of curvature
is_concave_up   = True
scene = my_scene.get_arc_mirror(scene, mirror_w, mirror_h,
               r, is_concave_up, add_brand_new=True)


# ========== SETUP FILE STRUCTURE SIM OF A SET OF SCENES ==========
mir_w_str = 'f'.join(f"{mirror_w:.1f}".split('.'))
mir_h_str = 'f'.join(f"{mirror_h:.1f}".split('.'))
concavity = 'up' if is_concave_up else 'down'
scene['name'] = f"concave_{concavity}_reflector_w_{mir_w_str}mm_h_{mir_h_str}mm"
try:
    dir_name = scene['name']
    os.makedirs(dir_name)
except FileExistsError:
    print(f"{dir_name} directory already exists.")

try:    
    print(f"{dir_name}/pics")
    os.makedirs(f"{dir_name}/pics")
except FileExistsError:
    print("pics sub-directory already exists.")



# ========== RUN SIM ==========
print("\n=== Simulation Running ===")
# Setup mirror translation params and preallocate space for output
pts_per_mm = 3
max_delta_X = 2 # mm; mirror's tangential displacement
num_rflt_positions = 2*max_delta_X*pts_per_mm+1
x = np.linspace(-max_delta_X, max_delta_X, num_rflt_positions)
P = np.zeros(num_rflt_positions)
num_bin_positions = np.int64(np.ceil(my_scene.detector_width/my_scene.bin_size))
irrad = np.zeros((num_rflt_positions, num_bin_positions))
readings = []

for idx, pos in enumerate(x): 
    if idx%4 == 0 :
        print(f"{idx/num_rflt_positions*100:02.1f}%", end='\r')
    # Vary Scene Parameters
    scene = my_scene.get_arc_mirror(scene, mirror_w, mirror_h,
               r, is_concave_up, x_offset=pos)

    scene["objs"][-1]["text"] = f"Mirror is\n{pos:.2f} mm\nfrom ctr"       
    file_name = f"{scene['name']}_mir_pos_{idx:03}"
    # print(scene)
    # with open('poo.json', 'w') as f:
    #     json.dump(scene, f)
    reading = simulate_scene(scene, file_name, dir_name)
    readings.append(reading)
    P[idx] = reading['power']
    irrad[idx,:] = reading['irradianceMap']


# ========== EXPORT DETECTOR DATA TO JSON ==========
readings_path = f"{dir_name}/{scene['name']}.json"
with open(os.path.join(os.getcwd(), readings_path), 'w', newline='') as file:
    json.dump(readings, file)

# ========== USE FFMPEG TO CREATE GIF FROM OUTPUT IMAGES ==========
ffmpeg_in = f"{dir_name}/pics/{scene['name']}_mir_pos_%3d.png"
ffmpeg_out = f"{dir_name}/{scene['name']}.gif"
create_gif_from_images(ffmpeg_in, ffmpeg_out)


# ========== USE DATA TO CREATE PLOTS ==========
#  Plot Power vs Tangential Reflector Displacement
power_fig = plt.figure()
plt.title("Power vs Tangential Reflector Displacement")
plt.plot(x, np.abs(P))
plt.grid(True)
plt.xlabel(r"$\Delta$x (mm from centre position)")
plt.ylabel("$Power$")
plt.savefig(f"{dir_name}/P_v_DeltaX_{scene['name']}.png")

irrad_fig = plt.figure()
b = np.arange(num_bin_positions)
bb, xx = np.meshgrid(b, x)
plt.title("(Line) Irradiance as a function of \nReflector Displacement and Bin Position")
plt.contourf(bb, xx, irrad)
plt.colorbar()
plt.grid(True)
plt.ylabel(r"$\Delta$x (mm from centre position)")
plt.xlabel(f"Bin Position (each bin is {my_scene.bin_size} mm)")
plt.xticks(b)
plt.savefig(f"{dir_name}/Irrad_Contour_{scene['name']}.png")

plt.show()


print("\nExamples completed!")

