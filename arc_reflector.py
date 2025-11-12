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
import time

run_sim_startup_checks()
scene = copy.deepcopy(my_scene.SCENE)
mirror_h        = 4.0     # mm; indicates the height of the mirror endpts
mirror_w        = 1.0     # mm
r               = 0.668    # mm; radius of curvature <<<<<<<<
d               = 0.22503     # mm <<<<<<<<<
is_concave_up   = False      # <<<<<<<<<
scene = my_scene.get_arc_mirror(scene, mirror_w, mirror_h,
               r, is_concave_up, add_brand_new=True)

concavity = 'up' if is_concave_up else 'down'
max_delta_Y = 4     # mm
v_pts_per_mm = 8            # <<<<<<<<<
heights = np.linspace(0,max_delta_Y,max_delta_Y*v_pts_per_mm+1)
print(heights, f"len({len(heights)})")
if concavity == 'up':       # line up the tops
    first_idx_gt_d = np.argmax(heights > d)
    heights = heights[first_idx_gt_d-1:]
    heights[0] = d
    print(heights, f"Index! {first_idx_gt_d} len({len(heights)})")
elif concavity == 'down':
    heights = heights[1:]
    heights[0] = 0
    heights[1:] -= d
    print(heights+d, f"len({len(heights)})")

#%%
mir_r_str = 'f'.join(f"{r:.4f}".split('.'))
try:
    main_dir_name = f"concave_{concavity}_r_{mir_r_str}mm"
    os.makedirs(main_dir_name)
except FileExistsError:
    print(f"{main_dir_name} directory already exists.")

top_file_names = []
for h in heights:
    # ========== SETUP FILE STRUCTURE SIM OF A SET OF SCENES ==========

    top = h
    if concavity == 'down':
        top += d
    mir_top_str = 'f'.join(f"{top:.4f}".split('.'))
    scene['name'] = f"concave_{concavity}_reflector_r_{mir_r_str}mm_top_{mir_top_str}mm"
    top_file_names.append(scene['name'])
    
    try:
        sub_dir_name = f"{main_dir_name}/{scene['name']}"
        os.makedirs(sub_dir_name)
    except FileExistsError:
        print(f"{sub_dir_name} directory already exists.")

    try:    
        print(f"{sub_dir_name}/pics")
        os.makedirs(f"{sub_dir_name}/pics")
    except FileExistsError:
        print("pics sub-directory already exists.")



    # ========== RUN SIM ==========
    print("\n=== Simulation Running ===")
    # Setup mirror translation params and preallocate space for output
    pts_per_mm = v_pts_per_mm
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
        scene = my_scene.get_arc_mirror(scene, mirror_w, h,
                r, is_concave_up, x_offset=pos)

        scene["objs"][-1]["text"] = f"r = {r:.4f} mm,\ntop = {top:.4f} mm,\nMirror is\n{pos:.2f} mm\nfrom ctr"             
        file_name = f"{scene['name']}_mir_pos_{idx:03}"
        reading = simulate_scene(scene, file_name, sub_dir_name)
        readings.append(reading)
        P[idx] = reading['power']
        irrad[idx,:] = reading['irradianceMap']

    # Record the end time
    end_time = time.perf_counter()
    # Calculate the duration
    duration = end_time - start_time
    print(f"Elapsed time: {duration:.6f} seconds")


    # ========== EXPORT DETECTOR DATA TO JSON ==========
    readings_path = f"{sub_dir_name}/{scene['name']}.json"
    with open(os.path.join(os.getcwd(), readings_path), 'w', newline='') as file:
        json.dump(readings, file)

    # ========== USE FFMPEG TO CREATE GIF FROM OUTPUT IMAGES ==========
    ffmpeg_in = f"{sub_dir_name}/pics/{scene['name']}_mir_pos_%3d.png"
    ffmpeg_out = f"{sub_dir_name}/{scene['name']}.gif"
    create_gif_from_images(ffmpeg_in, ffmpeg_out)


    # ========== USE DATA TO CREATE PLOTS ==========
    #  Plot Power vs Tangential Reflector Displacement
    power_fig = plt.figure()
    plt.title("Power vs Tangential Reflector Displacement")
    plt.plot(x, np.abs(P))
    plt.grid(True)
    plt.xlabel(r"$\Delta$x (mm from centre position)")
    plt.ylabel("$Power$")
    plt.savefig(f"{sub_dir_name}/P_v_DeltaX_{scene['name']}.png")

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
    plt.savefig(f"{sub_dir_name}/Irrad_Contour_{scene['name']}.png")

    # plt.show()


print("\nExamples completed!")
with open(f"{main_dir_name}/tops.json", 'w') as f:
    json.dump(top_file_names, f)
