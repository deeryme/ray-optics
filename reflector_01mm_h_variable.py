#!/usr/bin/env python3
"""
Ray Optics Simulation of tangential translation of reflector above photodetector
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from sim_helper_functions import run_sim_startup_checks, create_gif_from_images, simulate_scene
import basic_scene as my_scene
import json
import time


run_sim_startup_checks()
scene = my_scene.SCENE

# ========== SETUP FILE STRUCTURE SIM OF A SET OF SCENES ==========
mir_w_str = 'f'.join(f"{my_scene.mirror_width:.1f}".split('.'))
mir_h_str = 'f'.join(f"{my_scene.mirror_height:.1f}".split('.'))
scene['name'] = f"reflector_w_{mir_w_str}mm_h_{mir_h_str}mm"
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

# Record the start time
start_time = time.perf_counter()

for idx, pos in enumerate(x): 
    if idx%4 == 0 :
        print(f"{idx/num_rflt_positions*100:02.1f}%", end='\r')
    # Vary Scene Parameters
    scene["objs"][3]["p1"]["x"] = -my_scene.mirror_width/2 + pos
    scene["objs"][3]["p2"]["x"] =  my_scene.mirror_width/2 + pos
    scene["objs"][5]["text"] = f"Mirror is\n{pos:.2f} mm\nfrom ctr"       
    file_name = f"{scene['name']}_mir_pos_{idx:03}"
    reading = simulate_scene(scene, file_name, dir_name)
    readings.append(reading)
    P[idx] = reading['power']
    irrad[idx,:] = reading['irradianceMap']

# Record the end time
end_time = time.perf_counter()
# Calculate the duration
duration = end_time - start_time
print(f"Elapsed time: {duration:.6f} seconds")

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
plt.savefig(f"{dir_name}/pics/P_v_DeltaX_{scene['name']}.png")

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
plt.savefig(f"{dir_name}/pics/Irrad_Contour_{scene['name']}.png")

plt.show()


print("\nExamples completed!")

